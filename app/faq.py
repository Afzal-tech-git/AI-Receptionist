from typing import Dict
def get_faqs(client_cfg: Dict):
    return client_cfg.get("faqs", {})

def answer_faq(user_msg: str,client_cfg: Dict)->str | None:
    msg = user_msg.lower().strip()
    faqs = get_faqs(client_cfg)
    if any(k in msg for k in ["hour", "timing","open","band","close"]):
        return faqs.get("hours","Our hours are 9am-5pm, Mon-Fri.")
    if any(k in msg for k in ["sevices","kya","offer","packages"]):
        return faqs.get("services","We offer general consultation & follow-ups.")
    if any(k in msg for k in ["price","pricing","charges","cost"]):
        return faqs.get("pricing","Standard visit: $49, Follow-up: $29.")
    return None