
import re
from types import SimpleNamespace

RULES = [
    ("IT Support", "Network Issue",
     r"النت|انترنت|انترنت|الإنترنت|الانترنت|واي فاي|wifi|internet|network"),
    ("IT Support", "Printer Issue",
     r"برنتر|برينتر|طابع[هة]|printer|printing"),
    ("IT Support", "Computer Issue",
     r"كمبيوتر|كومبيوتر|لابتوب|حاسب|الشاش[هة]|monitor|computer|laptop"),
    ("IT Support", "Software Issue",
     r"سيستم|برنامج|باسورد|كلمة السر|software|password|login"),
    ("Maintenance", "Air Conditioning Issue",
     r"تكييف|التكييف|مكيف|تكييفات|air conditioning|\\bac\\b"),
    ("Maintenance", "Plumbing Issue",
     r"حنفي[هة]|مواسير|تسريب|بيسرب|السباك[هة]|صرف|plumbing|leak"),
    ("Maintenance", "Electrical Issue",
     r"لمب[هة]|إضاء[هة]|اضاء[هة]|كهربا|electric|lighting"),
    ("Maintenance", "Building Maintenance",
     r"باب|شباك|مقبض|كرسي مكسور|door|window"),
    ("Housekeeping", "Cleaning Issue",
     r"نظاف[هة]|تنضيف|تنظيف|ينضف|يتنضف|ننضف|تنضف|نضف|نضّف|زبال[هة]|قمام[هة]|cleaning|housekeeping"),
    ("Warehouse", "Stock Issue",
     r"المخزن|المخازن|صرف مستلزمات|المخزون|stock|warehouse"),
    ("Purchasing", "Purchasing Request",
     r"شراء|نشتري|مشتريات|توريد جديد|purchase|procurement"),
    ("Reception", "Reception Administration",
     r"حجز موعد|تسجيل استقبال|reception administration"),
]

SAFETY = (
    r"جهاز تنفس|جهاز التنفس|أكسجين|اكسجين|"
    r"جهاز أشعة|جهاز اشعة|جهاز تخدير|"
    r"حريق|دخان|ماس كهربائي|"
    r"ventilator|oxygen|fire|medical equipment"
)

def issue(message, category, department=None, decision="ROUTE", question=None):
    location = None
    match = re.search(
        r"(?:في|بـ|داخل)\\s+((?:مكتب|غرفة|حمام|الدور|الريسبشن|الاستقبال|العيادات|الأمن|الامن)[^،,.]*)",
        message
    )
    if match:
        location = match.group(1).strip()
    return SimpleNamespace(
        description=message,
        category=category,
        department=department,
        location=location,
        routing_decision=decision,
        clarification_question=question,
    )

def classify_request_demo(message):
    message = message.strip()
    if not message:
        return None

    if re.search(SAFETY, message, re.IGNORECASE):
        return SimpleNamespace(issues=[
            issue(message, "Safety Review", decision="REVIEW")
        ])

    matched = []
    for department, category, pattern in RULES:
        if re.search(pattern, message, re.IGNORECASE):
            if not any(x.category == category for x in matched):
                matched.append(issue(message, category, department))

    if not matched:
        return SimpleNamespace(issues=[
            issue(
                message,
                "Unclear Request",
                decision="CLARIFY",
                question="ممكن توضح نوع المشكلة أو الجهاز؟"
            )
        ])

    return SimpleNamespace(issues=matched)
