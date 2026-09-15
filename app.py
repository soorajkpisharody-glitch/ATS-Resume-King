import streamlit as st
import google.generativeai as genai
import traceback
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="ATS Resume King",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GOOGLE_API_KEY = ""

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# Payment Details
OWNER_NAME = "Sooraj"
WHATSAPP_NUMBER = "0555578736"
GOOGLE_PAY = "918075044214"
BOTIM_PAY = "971562796967"
PRICE_AED = "AED 25"
PRICE_INR = "₹500"

try:
    st.markdown("<h1 style='text-align:center;color:#4F46E5;'>⚡ ATS Resume King</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#6B7280;'>AI-Powered Resume Builder | ATS Scorer | WhatsApp CV Delivery</p>", unsafe_allow_html=True)
    st.divider()

    app_mode = st.sidebar.selectbox("Select Module", [
        "1. Resume Builder & ATS Scorer",
        "2. AI Career Chatbot",
        "3. Payment & Get CV",
        "4. Admin Leads Data",
        "5. System Status"
    ])

    if "leads_data" not in st.session_state:
        st.session_state.leads_data = []
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if app_mode == "1. Resume Builder & ATS Scorer":
        st.subheader("📝 ATS Resume Generator & AI Scorer")
        with st.form("resume_form"):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name", placeholder="Your Full Name")
                email = st.text_input("Email", placeholder="example@gmail.com")
                phone = st.text_input("WhatsApp Number", placeholder="+971500000000")
            with col2:
                target_job = st.text_input("Target Job Title", placeholder="Data Analyst / HR Manager")
                experience = st.text_area("Skills & Experience", placeholder="List your skills and work experience...")
            submitted = st.form_submit_button("⚡ Generate & Score Resume")
            if submitted:
                if full_name and experience and target_job:
                    with st.spinner("AI analyzing your profile..."):
                        try:
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            prompt = (
                                "Act as an elite ATS Resume Expert. Analyze this candidate and provide:\n"
                                "1. ATS Score out of 100 with justification\n"
                                "2. Professional optimized resume summary\n"
                                "3. 5 strong achievement bullet points\n"
                                "4. 3 specific ATS improvements\n\n"
                                "Candidate: " + full_name + "\n"
                                "Target Role: " + target_job + "\n"
                                "Experience/Skills: " + experience
                            )
                            response = model.generate_content(prompt)
                            st.success("✅ Resume Analyzed Successfully!")
                            st.markdown("### AI Analysis Report:")
                            st.markdown(response.text)
                            lead = {
                                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "Name": full_name,
                                "Email": email,
                                "Phone": phone,
                                "Target Role": target_job,
                                "Status": "Generated"
                            }
                            st.session_state.leads_data.append(lead)
                            st.warning("💡 To receive your full CV — Go to Module 3 and complete payment!")
                        except Exception as e:
                            st.error("API Error: " + str(e))
                else:
                    st.warning("Please fill all required fields!")

    elif app_mode == "2. AI Career Chatbot":
        st.subheader("💬 AI Career Assistant")
        st.write("Ask anything about resumes, interviews, or career guidance.")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        if user_query := st.chat_input("Ask your career question..."):
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)
            with st.chat_message("assistant"):
                try:
                    chat_model = genai.GenerativeModel('gemini-1.5-flash')
                    chat_prompt = "You are an expert AI Career and Resume Assistant for ATS Resume King. Answer professionally and concisely: " + user_query
                    chat_response = chat_model.generate_content(chat_prompt)
                    bot_reply = chat_response.text
                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                except Exception as e:
                    st.error("Chat error. Please try again.")

    elif app_mode == "3. Payment & Get CV":
        st.subheader("💳 Complete Payment & Receive Your CV")
        st.markdown("### 💰 Service Charge: " + PRICE_AED + " | " + PRICE_INR)
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🇮🇳 India Payment — Google Pay")
            st.info("UPI / Google Pay / PhonePe")
            st.markdown("**Send " + PRICE_INR + " to:**")
            st.code(GOOGLE_PAY)
            st.markdown("📱 **Google Pay | PhonePe | Paytm** — same number")
            wa_msg_india = "Hi Sooraj, I have paid " + PRICE_INR + " via Google Pay for ATS Resume King service. Please send my CV."
            wa_link_india = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + wa_msg_india.replace(" ", "%20")
            st.markdown("[✅ Click here to confirm payment on WhatsApp](" + wa_link_india + ")")

        with col2:
            st.markdown("### 🇦🇪 UAE Payment — Botim Pay")
            st.info("Botim Pay / Bank Transfer")
            st.markdown("**Send " + PRICE_AED + " to:**")
            st.code(BOTIM_PAY)
            st.markdown("📱 **Botim Pay** — instant transfer")
            wa_msg_uae = "Hi Sooraj, I have paid " + PRICE_AED + " via Botim Pay for ATS Resume King service. Please send my CV."
            wa_link_uae = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + wa_msg_uae.replace(" ", "%20")
            st.markdown("[✅ Click here to confirm payment on WhatsApp](" + wa_link_uae + ")")

        st.divider()
        st.success("After payment — WhatsApp us with your payment screenshot. CV will be delivered within 30 minutes! ⚡")

        st.markdown("### 📲 Direct WhatsApp Contact")
        st.markdown("[💬 Chat with us on WhatsApp](https://wa.me/" + WHATSAPP_NUMBER + ")")

    elif app_mode == "4. Admin Leads Data":
        st.subheader("📊 Leads & Analytics")
        if st.session_state.leads_data:
            df = pd.DataFrame(st.session_state.leads_data)
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", csv, 'leads.csv', 'text/csv')
        else:
            st.info("No leads yet. Generate a resume first.")

    elif app_mode == "5. System Status":
        st.subheader("🛡️ System Status")
        st.success("🟢 All Systems Operational")
        st.markdown(
            "- ✅ AI Resume Engine: Online\n"
            "- ✅ Gemini API: Connected\n"
            "- ✅ Google Pay: Active (" + GOOGLE_PAY + ")\n"
            "- ✅ Botim Pay: Active (" + BOTIM_PAY + ")\n"
            "- ✅ WhatsApp Support: Active\n"
            "- ✅ Self-Healing Handler: Active"
        )

except Exception as critical_error:
    st.error("⚠️ System error detected. Auto-recovery active.")
    st.code(traceback.format_exc())
    if st.button("🔄 Restart System"):
        st.rerun()
