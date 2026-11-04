"""Admin console for synthetic Nasaaem helpdesk data. Not suitable for real patient/staff data."""
import csv
import io
from contextlib import contextmanager
import streamlit as st
from psycopg.rows import dict_row
from prototype_cloud import get_prototype_connection

@contextmanager
def admin_connection(admin_id):
    with get_prototype_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT id FROM nasaaem_prototype.users
                           WHERE id = %s AND role='Admin' AND is_active=TRUE""", (admin_id,))
            if cur.fetchone() is None:
                raise PermissionError("Administrator access required")
        yield conn


def get_records(admin_id):
    with admin_connection(admin_id) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT id, username, full_name, phone_number, employee_id,
                       role, department, is_active
                FROM nasaaem_prototype.users ORDER BY id
            """)
            employees = [dict(x) for x in cur.fetchall()]
            cur.execute("""
                SELECT t.id AS ticket_id, t.request_id, t.created_at,
                       r.original_message, r.employee_id AS requester_identity,
                       COALESCE(u.full_name, r.employee_id) AS requester,
                       u.employee_id AS requester_employee_id,
                       t.description AS issue_description, t.category,
                       t.department AS assigned_department, t.location,
                       t.routing_decision, t.status, t.assigned_to,
                       f.solved AS feedback_solved, f.rating AS feedback_rating,
                       f.comment AS feedback_comment, f.updated_at AS feedback_updated_at,
                       COALESCE(conversation.messages, '') AS all_messages
                FROM nasaaem_prototype.tickets t
                JOIN nasaaem_prototype.requests r ON r.id=t.request_id
                LEFT JOIN nasaaem_prototype.users u
                     ON r.employee_id = ('USER-' || u.id::text)
                LEFT JOIN nasaaem_prototype.ticket_feedback f
                     ON f.ticket_id = t.id
                LEFT JOIN LATERAL (
                    SELECT string_agg(
                        to_char(m.created_at, 'YYYY-MM-DD HH24:MI') || ' | ' ||
                        COALESCE(author.full_name, 'Unknown') || ' (' ||
                        COALESCE(author.role, '?') || '): ' || m.body,
                        E'\n' ORDER BY m.created_at, m.id
                    ) AS messages
                    FROM nasaaem_prototype.ticket_messages m
                    LEFT JOIN nasaaem_prototype.users author ON author.id=m.author_id
                    WHERE m.ticket_id=t.id
                ) conversation ON TRUE
                ORDER BY t.id DESC
            """)
            tickets = [dict(x) for x in cur.fetchall()]
    return employees, tickets


def csv_bytes(rows, columns):
    output=io.StringIO(newline='')
    writer=csv.writer(output)
    writer.writerow(columns)
    for row in rows:
        cells=[]
        for column in columns:
            val=row.get(column)
            s='' if val is None else str(val)
            # Prevent CSV formula injection in Excel.
            if s.lstrip().startswith(('=', '+', '-', '@')):
                s="'"+s
            cells.append(s)
        writer.writerow(cells)
    return output.getvalue().encode('utf-8-sig')


def update_employee(admin_id, target_id, role, department, active, allowed_departments):
    if role not in {'Employee','Staff','Admin'}:
        raise ValueError('Invalid role')
    if department and department not in allowed_departments:
        raise ValueError('Invalid department')
    with admin_connection(admin_id) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT role, is_active FROM nasaaem_prototype.users WHERE id=%s FOR UPDATE', (target_id,))
            old=cur.fetchone()
            if not old:
                raise ValueError('User not found')
            if target_id == admin_id and (role != 'Admin' or not active):
                raise ValueError('You cannot remove your own admin access')
            if old['role']=='Admin' and old['is_active'] and (role != 'Admin' or not active):
                cur.execute("SELECT count(*) FROM nasaaem_prototype.users WHERE role='Admin' AND is_active=TRUE")
                if cur.fetchone()['count'] <= 1:
                    raise ValueError('Cannot disable the last active administrator')
            cur.execute('''UPDATE nasaaem_prototype.users
                           SET role=%s, department=%s, is_active=%s WHERE id=%s''',
                        (role, department, active, target_id))


def delete_ticket(admin_id, ticket_id):
    with admin_connection(admin_id) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM nasaaem_prototype.tickets WHERE id=%s FOR UPDATE', (ticket_id,))
            if not cur.fetchone():
                raise ValueError('Ticket not found')
            # Explicit child deletes, executed atomically; rollback on any FK error.
            cur.execute('DELETE FROM nasaaem_prototype.notifications WHERE ticket_id=%s', (ticket_id,))
            cur.execute('DELETE FROM nasaaem_prototype.ticket_feedback WHERE ticket_id=%s', (ticket_id,))
            cur.execute('DELETE FROM nasaaem_prototype.ticket_messages WHERE ticket_id=%s', (ticket_id,))
            cur.execute('DELETE FROM nasaaem_prototype.tickets WHERE id=%s', (ticket_id,))


def render_admin(user, allowed_departments):
    if user['role'] != 'Admin':
        st.error('Administrator access required')
        st.stop()
    st.title('Admin Control Center')
    st.caption('Nasaaem Helpdesk · Synthetic demonstration environment')
    try:
        employees, tickets = get_records(user['id'])
    except (PermissionError, Exception) as exc:
        st.error('Could not load administrative data: ' + type(exc).__name__)
        st.stop()

    active=sum(bool(r['is_active']) for r in employees)
    pending=sum(t['status'] not in ('Resolved','Closed') for t in tickets)
    c1,c2,c3,c4=st.columns(4)
    c1.metric('All Employees',len(employees))
    c2.metric('Active Accounts',active)
    c3.metric('Total Tickets',len(tickets))
    c4.metric('Open / Pending',pending)
    tab_tickets, tab_people, tab_manage = st.tabs(['Ticket Register','Employees Directory','Manage Records'])

    with tab_tickets:
        st.subheader('Complete Ticket Register')
        st.caption('Includes original employee request, assigned department, status, conversation, and feedback.')
        d1,d2=st.columns(2)
        departments=sorted({str(x['assigned_department']) for x in tickets if x['assigned_department']})
        statuses=sorted({str(x['status']) for x in tickets if x['status']})
        selected_department=d1.selectbox('Department',['All']+departments, key='admin_department_filter')
        selected_status=d2.selectbox('Status',['All']+statuses,key='admin_status_filter')
        search=st.text_input('Search ticket ID, requester, text or messages', key='admin_ticket_search')
        filtered=[r for r in tickets if
                  (selected_department=='All' or r['assigned_department']==selected_department) and
                  (selected_status=='All' or r['status']==selected_status) and
                  (not search or search.lower() in ' '.join(str(x) for x in r.values()).lower())]
        st.caption(f'{len(filtered)} of {len(tickets)} tickets shown')
        columns=['ticket_id','request_id','created_at','requester','requester_employee_id',
                 'original_message','issue_description','category','assigned_department','location',
                 'status','assigned_to','routing_decision','all_messages','feedback_solved',
                 'feedback_rating','feedback_comment','feedback_updated_at']
        if filtered:
            st.dataframe(filtered,hide_index=True,use_container_width=True)
        else:
            st.info('No matching tickets found.')
        st.download_button('Download ALL Tickets + Conversations (CSV)',
                           csv_bytes(tickets,columns),file_name='nasaaem_all_tickets_full.csv',
                           mime='text/csv',use_container_width=True,type='primary')
        st.download_button('Download FILTERED Tickets (CSV)',csv_bytes(filtered,columns),
                           file_name='nasaaem_filtered_tickets.csv',mime='text/csv',
                           use_container_width=True)
        if tickets:
            options={f"#{r['ticket_id']} — {r['requester']} — {r['status']}":r for r in tickets}
            chosen=st.selectbox('Inspect ticket and conversation',list(options),key='admin_ticket_inspect')
            selected=options[chosen]
            with st.container(border=True):
                st.markdown('**Original employee message**')
                st.write(selected['original_message'])
                st.markdown('**Ticket description**')
                st.write(selected['issue_description'])
                st.markdown('**Conversation history**')
                st.text(selected['all_messages'] or '(No conversation replies yet)')
                st.markdown('**Feedback**')
                st.write(selected['feedback_comment'] or '(No feedback yet)')

    with tab_people:
        st.subheader('Employees Directory')
        st.caption('All 150 original synthetic accounts, including inactive accounts and current role / department.')
        employee_filter=st.text_input('Search employees',key='admin_employee_search')
        filtered_employees=[r for r in employees if not employee_filter or
                            employee_filter.lower() in ' '.join(str(v) for v in r.values()).lower()]
        st.dataframe(filtered_employees,hide_index=True,use_container_width=True)
        user_columns=['id','username','full_name','employee_id','phone_number','role','department','is_active']
        st.download_button('Download ALL Employees (CSV)',csv_bytes(employees,user_columns),
                           file_name='nasaaem_all_employees.csv',mime='text/csv',
                           use_container_width=True,type='primary')

    with tab_manage:
        st.subheader('Manage Accounts and Tickets')
        st.warning('Synthetic data only. Role changes affect access immediately. Export CSV files before deleting records.')
        if employees:
            names={f"{r['id']} — {r['full_name']} ({r['employee_id']})":r for r in employees}
            label=st.selectbox('Choose employee',list(names),key='admin_manage_user')
            selected=names[label]
            departments=['No Department']+sorted(allowed_departments)
            initial_department=selected['department'] if selected['department'] in allowed_departments else 'No Department'
            with st.form('admin_edit_user_form'):
                new_role=st.selectbox('Role',['Employee','Staff','Admin'],
                    index=['Employee','Staff','Admin'].index(selected['role']))
                new_department=st.selectbox('Department',departments,index=departments.index(initial_department))
                active=st.checkbox('Active account',value=bool(selected['is_active']))
                promote=st.checkbox('I understand that Admin grants access to all prototype records')
                save=st.form_submit_button('Save employee changes',type='primary')
            if save:
                if new_role=='Admin' and selected['role']!='Admin' and not promote:
                    st.error('Confirm Admin role promotion first.')
                else:
                    try:
                        update_employee(user['id'],selected['id'],new_role,
                                        None if new_department=='No Department' else new_department,
                                        active,allowed_departments)
                    except Exception as exc:
                        st.error('Update failed: '+type(exc).__name__)
                    else:
                        st.success('Employee updated successfully.')
                        st.rerun()
            with st.expander('Delete employee access (reversible deactivation)'):
                st.caption('Preserves historic tickets and conversation attribution. The account can be reactivated above.')
                confirmation=st.text_input('Type DEACTIVATE '+str(selected['id']),key='admin_deactivate_confirm')
                if st.button('Deactivate selected account',key='admin_deactivate'):
                    if confirmation!='DEACTIVATE '+str(selected['id']):
                        st.error('Confirmation does not match.')
                    else:
                        try:
                            update_employee(user['id'],selected['id'],selected['role'],
                                            selected['department'],False,allowed_departments)
                        except Exception as exc:
                            st.error('Deactivation failed: '+type(exc).__name__)
                        else:
                            st.success('Account deactivated. No tickets were erased.')
                            st.rerun()
        st.divider()
        st.subheader('Permanently Delete a Ticket')
        st.caption('Deletes ticket, messages, feedback and ticket notifications. Cannot be undone.')
        if tickets:
            ticket_ids=[x['ticket_id'] for x in tickets]
            target=st.selectbox('Choose ticket to permanently delete',ticket_ids,key='admin_delete_ticket_id')
            confirm=st.text_input(f'Type DELETE {target}',key='admin_delete_ticket_confirm')
            if st.button('Permanently delete selected ticket',key='admin_delete_ticket_button'):
                if confirm!=f'DELETE {target}':
                    st.error('Confirmation does not match.')
                else:
                    try:
                        delete_ticket(user['id'],target)
                    except Exception as exc:
                        st.error('Ticket deletion failed; no partial deletion committed: '+type(exc).__name__)
                    else:
                        st.success('Ticket permanently deleted.')
                        st.rerun()
        else:
            st.info('No tickets available.')
