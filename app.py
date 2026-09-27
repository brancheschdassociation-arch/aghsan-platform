import streamlit as st
import anthropic

st.set_page_config(
    page_title="منصة الإدارة الذكية - جمعية أغصان",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
        html, body, [class*="css"] {
            direction: rtl;
            text-align: right;
            font-family: 'Cairo', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌱 منصة الإدارة الذكية - جمعية أغصان")
st.caption("مساعدك التنفيذي الذكي لإدارة المشاريع وصياغة التقارير")
st.divider()

st.subheader("💬 المساعد التنفيذي العام")
user_query = st.text_area("اكتبي طلبك أو استفسارك الإداري هنا:", height=150)

if st.button("إرسال الطلب لـ Claude", type="primary"):
    if not user_query:
        st.warning("الرجاء كتابة طلبك أولاً.")
    else:
        try:
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"]
            )

            system_prompt = """أنت مساعد إداري وتنفيذي ذكي وخبير في العمل الإنساني والتنموي، 
            تعمل لصالح جمعية فروع للتنمية والأعمال الخيرية (جمعية أغصان).
            المدير التنفيذي: نجاح قاسم. رئيس مجلس الإدارة: محمد بدوي.
            تقدم استشارات احترافية وتكتب مسودات لمشاريع تنموية وإغاثية،
            وتساعد في صياغة وثائق الامتثال المؤسسي باللغة العربية الرسمية السليمة."""

            with st.spinner("جاري الصياغة بواسطة Claude..."):
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=4000,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_query}]
                )

            final_text = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    final_text += block.text

            st.success("✨ تم إعداد الرد بنجاح:")
            st.markdown(final_text)

        except Exception as e:
            st.error(f"حدث خطأ: {e}")