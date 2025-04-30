import json
import re
import sys  # لإغلاق البرنامج

class LeaveChatbot:
    def __init__(self, responses_file="responses.json"):
        with open(responses_file, "r", encoding="utf-8") as file:
            self.responses = json.load(file)

    def normalize_input(self, text):
        # Remove diacritics, punctuation, and convert Arabic letters to a standard form
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
        replacements = {
            "إ": "ا",
            "أ": "ا",
            "آ": "ا",
            "ى": "ي",
            "ة": "ه",
            "ٱ": "ا",
            "ذ": "د",
            "ٰ": "",
            "ـ": "",
            "ْ": "", "ٌ": "", "ٍ": "", "ً": "", "ُ": "", "ِ": "", "َ": "", "ّ": ""
        }
        for src, target in replacements.items():
            text = text.replace(src, target)
        return text

    def get_response(self, user_input):
        normalized = self.normalize_input(user_input)



        # إجازة اعتيادية
        if (
            any(word in normalized for word in ["معلومات", "تفاصيل", "ايه هي", "ما هي"]) and
            any(word in normalized for word in ["اعتيادية", "اعتيادي", "عادية", "عادي"])
        ):
            return self.responses.get("normalData")

        # إجازة عارضة
        if (
            any(word in normalized for word in ["معلومات", "تفاصيل", "ايه هي", "ما هي"]) and
            any(word in normalized for word in ["عارضه", "عارضة"])
        ):
            return self.responses.get("casualData")

        # إجازة مرضية
        if (
            any(word in normalized for word in ["معلومات", "تفاصيل", "ايه هي", "ما هي"]) and
            any(word in normalized for word in ["مرضي", "مرضية", "مرض"])
        ):
            return self.responses.get("sickData")

        # إجازة وضع
        if (
            any(word in normalized for word in ["معلومات", "تفاصيل", "ايه هي", "ما هي"]) and
            any(word in normalized for word in ["وضع", "ولادة", "حمل"])
        ):
            return self.responses.get("maternityData")

        # إجازة حج أو عمرة
        if (
            any(word in normalized for word in ["معلومات", "تفاصيل", "ايه هي", "ما هي"]) and
            any(word in normalized for word in ["حج", "عمرة"])
        ):
            return self.responses.get("hajjData")

        # إجازة بدون مرتب
        if (
            any(word in normalized for word in ["معلومات", "تفاصيل", "ايه هي", "ما هي"]) and
            any(word in normalized for word in ["بدون", "غير", "بدون_مرتب", "بدون مرتب"])
        ):
            return self.responses.get("unpaidData")

        # إجازة حداد (وفاة)
        if (
            any(word in normalized for word in ["معلومات", "تفاصيل", "ايه هي", "ما هي"]) and
            any(word in normalized for word in ["وفاة", "وفاه", "حداد", "ميت", "موت"])
        ):
            return self.responses.get("deathData")

        # إجازة زواج
        if (
            any(word in normalized for word in ["معلومات", "تفاصيل", "ايه هي", "ما هي"]) and
            any(word in normalized for word in ["زواج", "جواز", "فرح"])
        ):
            return self.responses.get("marriageData")

        # إجازة امتحانات
        if (
            any(word in normalized for word in ["معلومات", "تفاصيل", "ايه هي", "ما هي"]) and
            any(word in normalized for word in ["امتحانات", "امتحان", "اختبار"])
        ):
            return self.responses.get("examData")

        # تصريح خروج (إجازة قصيرة)
        if (
            any(word in normalized for word in ["معلومات", "تفاصيل", "ايه هي", "ما هي"]) and
            any(word in normalized for word in ["تصريح", "خروج", "قصيره", "قصيرة"])
        ):
            return self.responses.get("permissionData")


        # التعامل مع سؤال هل يعرف الإجازات
        if any(phrase in normalized for phrase in ["تعرف اجازات", "عارف اجازات", "تفهم في الاجازات","تفهم الاجازات" ,"عندك معلومات عن الاجازات", "انت على معرفه بالاجازات"]):
            return "نعم، لدي معرفة بجميع أنواع الإجازات وفقًا للقانون المصري. ما سؤالك؟"
        
        # التعامل مع التحية
        if any(word in normalized for word in ["اهلا", "مرحبا", "السلام عليكم", "هاي", "ازيك", "صباح الخير", "مساء الخير"]):
            return "أهلاً بك! كيف يمكنني مساعدتك بخصوص الإجازات؟"
        if any(word in normalized for word in ["كيف حالك"]):
            return " بخير الحمد لله! كيف يمكنني مساعدتك بخصوص الإجازات؟"
        
        # نهاية المحادثة
        if any(word in normalized for word in ["شكرا", "شكر", "مشكور", "يسلمو", "يعطيك العافيه","كتر خيرك","حبيبي", "تسلم"]):
            return self.responses.get("thanks")

        # التعامل مع الاستفسارات العامة
        if any(word in normalized for word in ["عام", "معلومات عامة","معلومات","عامة","القانون","انواع"]):
            return self.responses.get("general_info")

        # التعامل مع الاستفسارات القانونية
        elif any(word in normalized for word in ["قانون", "مراجع قانونية"]):
            return self.responses.get("legal_reference")
        

        if any(word in normalized for word in ["اعتياديه", "اعتيادي", "عاديه" ,"عادي"]):
            return self.responses.get("normal_leave")
        elif any(word in normalized for word in ["عارضه", "عارضة", "عرض", "عارض"]):
            return self.responses.get("casual_leave")
        elif any(word in normalized for word in ["مرضي", "مرضيه", "تقرير","عيان","مريض"]):
            return self.responses.get("sick_leave")
        elif any(word in normalized for word in ["وضع", "ولاده", "الولادة"]):
            return self.responses.get("maternity_leave")
        elif any(word in normalized for word in ["حج", "عمره", "عمرة"]):
            return self.responses.get("hajj_leave")
        elif any(word in normalized for word in ["بدون مرتب", "بدون اجر", "اجازه خاصه"]):
            return self.responses.get("unpaid_leave")
        elif any(word in normalized for word in ["وفاه", "وفاة", "حداد", "ميت"]):
            return self.responses.get("death_leave")
        elif any(word in normalized for word in ["زواج", "جواز", "فرح", "عريس"]):
            return self.responses.get("marriage_leave")
        elif any(word in normalized for word in ["امتحان", "امتحانات", "اختبار"]):
            return self.responses.get("exam_leave")
        elif any(word in normalized for word in ["تصريح", "ساعتين", "اجازه قصيره", "خروج مؤقت", "خروج ساعتين"]):
            return self.responses.get("permission_leave")
        else:
            return "عذرًا، لم أفهم طلبك"
