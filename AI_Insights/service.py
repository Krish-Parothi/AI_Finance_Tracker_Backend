# from datetime import datetime
# from collections import defaultdict
# from app.db import expenses
# from bson import ObjectId

# class InsightsService:

#     @staticmethod
#     def get_category_trends(user_id):
#         cursor = expenses.find({"user_id": ObjectId(user_id)})
#         monthly = defaultdict(lambda: defaultdict(int))

#         for doc in cursor:
#             d = datetime.strptime(doc["date"], "%Y-%m-%d")
#             key = d.strftime("%b")
#             monthly[key][doc["category"]] += doc["amount"]

#         out = []
#         for month in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]:
#             if month in monthly:
#                 entry = {"month": month}
#                 entry.update(monthly[month])
#                 out.append(entry)
#         return out

#     @staticmethod
#     def get_daily_spending(user_id):
#         cursor = expenses.find({"user_id": ObjectId(user_id)})
#         days = defaultdict(int)

#         for doc in cursor:
#             days[doc["date"]] += doc["amount"]

#         return [
#             {"date": d, "amount": amt}
#             for d, amt in sorted(days.items())
#         ]

#     @staticmethod
#     def get_category_distribution(user_id):
#         cursor = expenses.find({"user_id": ObjectId(user_id)})
#         totals = defaultdict(int)
#         overall = 0

#         for doc in cursor:
#             totals[doc["category"]] += doc["amount"]
#             overall += doc["amount"]

#         out = []
#         for cat, amt in totals.items():
#             pct = round((amt / overall) * 100, 2) if overall else 0
#             out.append({
#                 "category": cat,
#                 "percentage": pct
#             })
#         return out

#     @staticmethod
#     def get_recommendations(user_id):
#         dist = InsightsService.get_category_distribution(user_id)
#         if not dist:
#             return []

#         max_cat = max(dist, key=lambda x: x["percentage"])

#         recs = [
#             {
#                 "priority": "high",
#                 "title": f"High spending in {max_cat['category']}",
#                 "description": f"{max_cat['percentage']}% of total spending."
#             }
#         ]

#         return recs




# from datetime import datetime
# from collections import defaultdict
# from app.db import expenses
# from bson import ObjectId

# class InsightsService:

#     @staticmethod
#     def get_category_trends(user_id):
#         cursor = expenses.find({"user_id": ObjectId(user_id)})
#         monthly = defaultdict(lambda: defaultdict(int))

#         for doc in cursor:
#             ts = doc.get("timestamp")
#             if not ts:
#                 continue
#             cat = doc.get("category")
#             if not cat:
#                 continue

#             key = ts.strftime("%b")
#             monthly[key][cat] += doc.get("amount", 0)

#         out = []
#         for m in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]:
#             if m in monthly:
#                 e = {"month": m}
#                 e.update(monthly[m])
#                 out.append(e)
#         return out

#     @staticmethod
#     def get_daily_spending(user_id):
#         cursor = expenses.find({"user_id": ObjectId(user_id)})
#         days = defaultdict(int)

#         for doc in cursor:
#             ts = doc.get("timestamp")
#             if not ts:
#                 continue
#             key = ts.strftime("%Y-%m-%d")
#             days[key] += doc.get("amount", 0)

#         return [{"date": d, "amount": a} for d, a in sorted(days.items())]

#     @staticmethod
#     def get_category_distribution(user_id):
#         cursor = expenses.find({"user_id": ObjectId(user_id)})
#         totals = defaultdict(int)
#         overall = 0

#         for doc in cursor:
#             cat = doc.get("category")
#             if not cat:
#                 continue
#             amt = doc.get("amount", 0)
#             totals[cat] += amt
#             overall += amt

#         out = []
#         for cat, amt in totals.items():
#             pct = round((amt / overall) * 100, 2) if overall else 0
#             out.append({"category": cat, "percentage": pct})
#         return out

#     @staticmethod
#     def get_recommendations(user_id):
#         dist = InsightsService.get_category_distribution(user_id)
#         if not dist:
#             return []

#         max_cat = max(dist, key=lambda x: x["percentage"])

#         return [{
#             "priority": "high",
#             "title": f"High spending in {max_cat['category']}",
#             "description": f"{max_cat['percentage']}% of total spending."
#         }]



from datetime import datetime
from collections import defaultdict
from app.db import expenses
from bson import ObjectId


class InsightsService:

    @staticmethod
    def get_category_trends(user_id):
        cursor = expenses.find({"user_id": ObjectId(user_id)})
        monthly = defaultdict(lambda: defaultdict(int))

        for doc in cursor:
            ts = doc.get("timestamp")
            if not ts:
                continue
            if isinstance(ts, str):
                try:
                    ts = datetime.fromisoformat(ts)
                except:
                    continue

            cat = doc.get("category")
            if not cat:
                continue

            key = ts.strftime("%b")
            monthly[key][cat] += doc.get("amount", 0)

        out = []
        for m in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]:
            if m in monthly:
                e = {"month": m}
                e.update(monthly[m])
                out.append(e)
        return out


    @staticmethod
    def get_daily_spending(user_id):
        cursor = expenses.find({"user_id": ObjectId(user_id)})
        days = defaultdict(int)

        for doc in cursor:
            ts = doc.get("timestamp")
            if not ts:
                continue
            if isinstance(ts, str):
                try:
                    ts = datetime.fromisoformat(ts)
                except:
                    continue

            key = ts.strftime("%Y-%m-%d")
            days[key] += doc.get("amount", 0)

        return [{"date": d, "amount": a} for d, a in sorted(days.items())]


    @staticmethod
    def get_category_distribution(user_id):
        cursor = expenses.find({"user_id": ObjectId(user_id)})
        totals = defaultdict(int)
        overall = 0

        for doc in cursor:
            cat = doc.get("category")
            if not cat:
                continue
            amt = doc.get("amount", 0)
            totals[cat] += amt
            overall += amt

        out = []
        for cat, amt in totals.items():
            pct = round((amt / overall) * 100, 2) if overall else 0
            out.append({"category": cat, "percentage": pct})
        return out


    @staticmethod
    def get_recommendations(user_id):
        dist = InsightsService.get_category_distribution(user_id)
        if not dist:
            return []

        max_cat = max(dist, key=lambda x: x["percentage"])

        return [{
            "priority": "high",
            "title": f"High spending in {max_cat['category']}",
            "description": f"{max_cat['percentage']}% of total spending."
        }]
