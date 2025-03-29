import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ✅ Must be the first Streamlit command
st.set_page_config("Pakistan Income Tax Estimator", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
        body {
            background-color: #f2f6ff;
        }
        .stApp {
            background-color: #f5f7fa;
            color: #2c3e50;
            font-family: 'Segoe UI', sans-serif;
        }
        .css-18e3th9 {
            background: #e8f0fe;
        }
        .css-1d391kg {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        }
    </style>
""", unsafe_allow_html=True)

# --- Tax Calculation Logic ---
def calculate_tax(income):
    tax = 0
    if income <= 1_000_000:
        tax = 0
    elif income <= 5_000_000:
        tax = (income - 1_000_000) * 0.10
    elif income <= 10_000_000:
        tax = (4_000_000 * 0.10) + (income - 5_000_000) * 0.20
    else:
        tax = (4_000_000 * 0.10) + (5_000_000 * 0.20) + (income - 10_000_000) * 0.30
    return tax

def detailed_tax_breakdown(income):
    slabs = [
        (1_000_000, 0),
        (5_000_000, 0.10),
        (10_000_000, 0.20),
        (float('inf'), 0.30)
    ]
    breakdown = []
    remaining_income = income
    previous_limit = 0

    for limit, rate in slabs:
        slab_range = limit - previous_limit
        if remaining_income > 0:
            taxable_amount = min(remaining_income, slab_range)
            tax_for_this_bracket = taxable_amount * rate
            breakdown.append({
                "Bracket (PKR)": f"₨{previous_limit:,.0f} - ₨{limit:,.0f}",
                "Rate": f"{rate*100:.0f}%",
                "Tax (PKR)": f"₨{tax_for_this_bracket:,.0f}"
            })
            remaining_income -= taxable_amount
            previous_limit = limit
        else:
            break
    return breakdown

def get_tax_tips(taxable_income):
    tips = []
    if taxable_income > 600_000:
        tips.append("📚 Invest in tax-exempt savings schemes like Behbood or Pensioners’ Benefit Account.")
    if taxable_income > 1_000_000:
        tips.append("🏥 Utilize Section 60D: Claim deductions on health insurance premiums.")
    if taxable_income > 2_000_000:
        tips.append("🏠 Consider investing in property under tax rebate schemes.")
    if taxable_income < 1_000_000:
        tips.append("✅ You are exempt from income tax.")
    return tips

# --- UI Layout ---
st.title("💼 Pakistan Income Tax Estimator")
st.markdown("Calculate your estimated tax, view slab breakdowns, and get personalized tips to save tax.")

# --- Sidebar Inputs ---
st.sidebar.header("🧾 Enter Your Info")
income = st.sidebar.number_input("Annual Income (PKR)", min_value=0, step=50_000, value=5_000_000)
deductions = st.sidebar.number_input("Deductions (PKR)", min_value=0, step=50_000, value=0)

# --- Calculations ---
taxable_income = max(income - deductions, 0)
tax = calculate_tax(taxable_income)
effective_tax_rate = (tax / income * 100) if income > 0 else 0
monthly_tax = tax / 12

# --- Summary Metrics ---
st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₨{income:,.0f}")
col2.metric("Deductions", f"₨{deductions:,.0f}")
col3.metric("Taxable Income", f"₨{taxable_income:,.0f}")

st.markdown(f"### 💸 Estimated Annual Tax: **₨{tax:,.0f}**")
st.markdown(f"📆 Monthly Tax: **₨{monthly_tax:,.0f}** | Effective Tax Rate: **{effective_tax_rate:.2f}%**")

# --- Pie Chart ---
st.subheader("🧁 Income Distribution")
labels = ['Tax', 'Deductions', 'Remaining Income']
values = [tax, deductions, income - tax - deductions]
colors = ['#ff6b6b', '#4ecdc4', '#1a535c']
fig, ax = plt.subplots()
ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
ax.axis('equal')
st.pyplot(fig)

# --- Detailed Tax Breakdown ---
st.subheader("📋 Detailed Tax Breakdown")
breakdown = detailed_tax_breakdown(taxable_income)
df = pd.DataFrame(breakdown)
st.dataframe(df, use_container_width=True)

# --- Tax Slabs Info ---
with st.expander("📚 View Tax Slabs (PKR)"):
    st.markdown("""
    - **₨0 – ₨1,000,000**: 0%  
    - **₨1,000,001 – ₨5,000,000**: 10%  
    - **₨5,000,001 – ₨10,000,000**: 20%  
    - **Above ₨10,000,000**: 30%
    """)

# --- Tax Saving Tips ---
st.subheader("💡 Tax Saving Tips")
tips = get_tax_tips(taxable_income)
if tips:
    for tip in tips:
        st.markdown(f"- {tip}")
else:
    st.markdown("✅ You are already in a no/low tax bracket.")

# --- Export Report ---
st.subheader("📤 Export")
export_df = pd.DataFrame({
    "Field": ["Annual Income", "Deductions", "Taxable Income", "Estimated Tax", "Monthly Tax", "Effective Tax Rate"],
    "Amount": [f"₨{income:,.0f}", f"₨{deductions:,.0f}", f"₨{taxable_income:,.0f}", f"₨{tax:,.0f}", f"₨{monthly_tax:,.0f}", f"{effective_tax_rate:.2f}%"]
})
st.download_button("📄 Download Tax Report (CSV)", export_df.to_csv(index=False).encode('utf-8'), file_name="tax_report.csv")

st.markdown("---")
st.caption("📌 This tool uses simplified slabs. Please consult a tax consultant for official filing.")
