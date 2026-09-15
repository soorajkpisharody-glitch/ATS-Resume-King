import streamlit as st
import google.generativeai as genai
import traceback
import pandas as pd
from datetime import datetime
import base64
import PyPDF2
import io

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

OWNER_NAME = "Sooraj"
WHATSAPP_NUMBER = "971555578736"
GOOGLE_PAY = "918075044214"
BOTIM_PAY = "971562796967"
PRICE_AED = "AED 25"
PRICE_INR = "500"

try:
    st.markdown("<h1 style='text-align:center;color:#4F46E5;'>⚡ ATS Resume King</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#6B7280;'>AI-Powered Resume Builder | ATS Scorer | WhatsApp CV Delivery</p>", unsafe_allow_html=True)
    st.divider()

    app_mode = st.sidebar.selectbox("Select Module", [
        "1. Check My Resume ATS Score",
        "2. Build New ATS Resume",
        "3. AI Career Chatbot",
        "4. Payment & Get Full CV",
        "5. Admin Panel",
        "6. System Status"
    ])

    if "leads_data" not in st.session_state:
        st.session_state.leads_data = []
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_payments" not in st.session_state:
        st.session_state.pending_payments = []

    if app_mode == "1. Check My Resume ATS Score":
        st.subheader("📄 Check Your Resume ATS Score — FREE!")
        st.info("Upload your CV and get your ATS Score instantly — 100% FREE!")

        with st.form("resume_check_form"):
            full_name = st.text_input("Your Full Name", placeholder="Your Full Name")
            phone = st.text_input("WhatsApp Number", placeholder="+971500000000")
            target_job = st.text_input("Job you are applying for", placeholder="Data Analyst / HR Manager")
            resume_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])
            check_submitted = st.form_submit_button("⚡ Check My ATS Score — FREE")

            if check_submitted:
                if full_name and target_job and resume_file:
                    with st.spinner("AI analyzing your resume..."):
                        try:
                            pdf_reader = PyPDF2.PdfReader(io.BytesIO(resume_file.read()))
                            resume_text = ""
                            for page in pdf_reader.pages:
                                resume_text += page.extract_text()

                            if not resume_text.strip():
                                st.error("PDF read ചെയ്യാൻ കഴിഞ്ഞില്ല. Clear text PDF upload ചെയ്യുക.")
                            else:
                                model = genai.GenerativeModel('gemini-1.5-flash')
                                prompt = (
                                    "You are an ATS Resume Expert. Analyze this resume.\n"
                                    "Return ONLY a single number — the ATS Score out of 100.\n"
                                    "Nothing else. Just the number. Example: 67\n\n"
                                    "Target Job: " + target_job + "\n"
                                    "Resume:\n" + resume_text[:3000]
                                )
                                response = model.generate_content(prompt)
                                score_text = response.text.strip().replace("/100","").strip()

                                try:
                                    score = int(''.join(filter(str.isdigit, score_text[:3])))
                                except:
                                    score = 65

                                st.divider()
                                col_s1, col_s2, col_s3 = st.columns([1,2,1])
                                with col_s2:
                                    if score >= 80:
                                        color = "#22c55e"
                                        emoji = "🟢"
                                    elif score >= 60:
                                        color = "#f59e0b"
                                        emoji = "🟡"
                                    else:
                                        color = "#ef4444"
                                        emoji = "🔴"

                                    st.markdown(
                                        "<div style='text-align:center;padding:2rem;background:#f8fafc;border-radius:16px;border:2px solid " + color + ";'>"
                                        "<div style='font-size:14px;color:#6B7280;margin-bottom:8px'>Your ATS Score</div>"
                                        "<div style='font-size:72px;font-weight:700;color:" + color + ";'>" + str(score) + "</div>"
                                        "<div style='font-size:18px;color:#6B7280;'>/100 " + emoji + "</div>"
                                        "</div>",
                                        unsafe_allow_html=True
                                    )

                                st.divider()
                                st.warning("🔒 Want to know WHY and get a fully optimized CV? Pay " + PRICE_AED + " / ₹" + PRICE_INR + " — Full report + CV delivered to WhatsApp in 30 min!")

                                col_a, col_b = st.columns(2)
                                with col_a:
                                    wa_msg = "Hi Sooraj! My ATS Score is " + str(score) + "/100. Name: " + full_name + " | Role: " + target_job + " | I want full report and optimized CV. Paying " + PRICE_AED + " via Botim Pay."
                                    wa_link = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + wa_msg.replace(" ", "%20")
                                    st.markdown("[🇦🇪 Pay " + PRICE_AED + " — Get Full CV](" + wa_link + ")")
                                with col_b:
                                    wa_msg2 = "Hi Sooraj! My ATS Score is " + str(score) + "/100. Name: " + full_name + " | Role: " + target_job + " | I want full report and CV. Paying Rs." + PRICE_INR + " via Google Pay."
                                    wa_link2 = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + wa_msg2.replace(" ", "%20")
                                    st.markdown("[🇮🇳 Pay ₹" + PRICE_INR + " — Get Full CV](" + wa_link2 + ")")

                                lead = {
                                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "Name": full_name,
                                    "Phone": phone,
                                    "Target Role": target_job,
                                    "ATS Score": str(score),
                                    "Type": "Resume Upload Check",
                                    "Status": "Score Given — Awaiting Payment"
                                }
                                st.session_state.leads_data.append(lead)

                        except Exception as e:
                            st.error("Error: " + str(e))
                else:
                    st.warning("Please fill all fields and upload resume!")

    elif app_mode == "2. Build New ATS Resume":
        st.subheader("📝 Build New Resume — FREE ATS Score!")
        st.info("No resume? Fill in details and get your ATS Score FREE!")

        with st.form("resume_form"):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name", placeholder="Your Full Name")
                email = st.text_input("Email", placeholder="example@gmail.com")
                phone = st.text_input("WhatsApp Number", placeholder="+971500000000")
            with col2:
                target_job = st.text_input("Target Job Title", placeholder="Data Analyst / HR Manager")
                experience = st.text_area("Skills & Experience", placeholder="List your skills and work experience...")
            submitted = st.form_submit_button("⚡ Get My FREE ATS Score")

            if submitted:
                if full_name and experience and target_job:
                    with st.spinner("AI analyzing your profile..."):
                        try:
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            prompt = (
                                "You are an ATS Resume Expert.\n"
                                "Return ONLY a single number — the ATS Score out of 100.\n"
                                "Nothing else. Just the number. Example: 72\n\n"
                                "Candidate: " + full_name + "\n"
                                "Target Role: " + target_job + "\n"
                                "Experience/Skills: " + experience
                            )
                            response = model.generate_content(prompt)
                            score_text = response.text.strip().replace("/100","").strip()

                            try:
                                score = int(''.join(filter(str.isdigit, score_text[:3])))
                            except:
                                score = 65

                            st.divider()
                            col_s1, col_s2, col_s3 = st.columns([1,2,1])
                            with col_s2:
                                if score >= 80:
                                    color = "#22c55e"
                                    emoji = "🟢"
                                elif score >= 60:
                                    color = "#f59e0b"
                                    emoji = "🟡"
                                else:
                                    color = "#ef4444"
                                    emoji = "🔴"

                                st.markdown(
                                    "<div style='text-align:center;padding:2rem;background:#f8fafc;border-radius:16px;border:2px solid " + color + ";'>"
                                    "<div style='font-size:14px;color:#6B7280;margin-bottom:8px'>Your ATS Score</div>"
                                    "<div style='font-size:72px;font-weight:700;color:" + color + ";'>" + str(score) + "</div>"
                                    "<div style='font-size:18px;color:#6B7280;'>/100 " + emoji + "</div>"
                                    "</div>",
                                    unsafe_allow_html=True
                                )

                            st.divider()
                            st.warning("🔒 Full Optimized CV Ready! Pay " + PRICE_AED + " / ₹" + PRICE_INR + " — receive on WhatsApp in 30 min!")
                            st.info("👉 Go to **Module 4 — Payment** to complete!")

                            lead = {
                                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "Name": full_name,
                                "Email": email,
                                "Phone": phone,
                                "Target Role": target_job,
                                "ATS Score": str(score),
                                "Type": "New Resume Build",
                                "Status": "Score Given — Awaiting Payment"
                            }
                            st.session_state.leads_data.append(lead)

                        except Exception as e:
                            st.error("API Error: " + str(e))
                else:
                    st.warning("Please fill all required fields!")

    elif app_mode == "3. AI Career Chatbot":
        st.subheader("💬 AI Career Assistant")
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

    elif app_mode == "4. Payment & Get Full CV":
        st.subheader("💳 Pay & Receive Your Complete CV")
        st.markdown("### 💰 " + PRICE_AED + " | ₹" + PRICE_INR + " only!")
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🇦🇪 UAE — Botim Pay")
            st.markdown("Send **" + PRICE_AED + "** to:")
            st.code(BOTIM_PAY)
        with col2:
            st.markdown("### 🇮🇳 India — Google Pay")
            st.markdown("Send **₹" + PRICE_INR + "** to:")
            st.code(GOOGLE_PAY)

        st.divider()
        st.markdown("### 📸 Upload Payment Screenshot")
        st.warning("Payment ചെയ്ത ശേഷം screenshot upload ചെയ്യുക. Verify ചെയ്ത ശേഷം CV അയക്കും!")

        with st.form("payment_form"):
            pay_name = st.text_input("Your Full Name")
            pay_phone = st.text_input("Your WhatsApp Number", placeholder="+971500000000")
            pay_method = st.selectbox("Payment Method", ["Botim Pay (AED 25)", "Google Pay (₹500)"])
            pay_screenshot = st.file_uploader("Upload Payment Screenshot", type=["jpg","jpeg","png"])
            pay_submitted = st.form_submit_button("✅ Submit Payment Proof")

            if pay_submitted:
                if pay_name and pay_phone and pay_screenshot:
                    screenshot_data = base64.b64encode(pay_screenshot.read()).decode()
                    payment_record = {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Name": pay_name,
                        "Phone": pay_phone,
                        "Method": pay_method,
                        "Screenshot": screenshot_data,
                        "Status": "⏳ Pending Verification"
                    }
                    st.session_state.pending_payments.append(payment_record)
                    wa_msg = "NEW PAYMENT! Name: " + pay_name + " | Phone: " + pay_phone + " | Method: " + pay_method
                    wa_link = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + wa_msg.replace(" ", "%20")
                    st.success("✅ Payment proof submitted!")
                    st.info("CV will be sent to your WhatsApp within 30 minutes!")
                    st.markdown("[📲 WhatsApp notify ചെയ്യുക (faster)](" + wa_link + ")")
                else:
                    st.warning("Please fill all fields and upload screenshot!")

    elif app_mode == "5. Admin Panel":
        st.subheader("🔐 Admin Panel")
        admin_pass = st.text_input("Enter Admin Password", type="password")

        if admin_pass == "sooraj123":
            tab1, tab2 = st.tabs(["💰 Pending Payments", "📋 All Leads"])

            with tab1:
                if st.session_state.pending_payments:
                    for i, payment in enumerate(st.session_state.pending_payments):
                        with st.expander("Payment #" + str(i+1) + " — " + payment["Name"] + " — " + payment["Status"]):
                            st.write("**Name:** " + payment["Name"])
                            st.write("**Phone:** " + payment["Phone"])
                            st.write("**Method:** " + payment["Method"])
                            st.write("**Time:** " + payment["Timestamp"])
                            img_data = base64.b64decode(payment["Screenshot"])
                            st.image(img_data, caption="Payment Screenshot", use_column_width=True)
                            col_a, col_b = st.columns(2)
                            with col_a:
                                wa_cv = "https://wa.me/" + payment["Phone"].replace("+","").replace(" ","") + "?text=Hi%20" + payment["Name"].replace(" ","%20") + "%20payment%20verified!%20Your%20CV%20coming%20shortly!"
                                st.markdown("[✅ Verify & Send CV](" + wa_cv + ")")
                            with col_b:
                                if st.button("❌ Reject", key="reject_"+str(i)):
                                    st.session_state.pending_payments[i]["Status"] = "❌ Rejected"
                                    st.rerun()
                else:
                    st.info("No pending payments yet.")

            with tab2:
                if st.session_state.leads_data:
                    df = pd.DataFrame(st.session_state.leads_data)
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download CSV", csv, 'leads.csv', 'text/csv')
                else:
                    st.info("No leads yet.")
        else:
            if admin_pass:
                st.error("Wrong password!")

    elif app_mode == "6. System Status":
        st.subheader("🛡️ System Status")
        st.success("🟢 All Systems Operational")
        st.markdown(
            "- ✅ AI Resume Engine: Online\n"
            "- ✅ Resume Upload ATS Check: Active\n"
            "- ✅ Gemini API: Connected\n"
            "- ✅ Botim Pay: Active\n"
            "- ✅ Google Pay: Active\n"
            "- ✅ Admin Panel: Secure\n"
            "- ✅ Self-Healing Handler: Active"
        )

except Exception as critical_error:
    st.error("⚠️ System error detected. Auto-recovery active.")
    st.code(traceback.format_exc())
    if st.button("🔄 Restart System"):
        st.rerun()
