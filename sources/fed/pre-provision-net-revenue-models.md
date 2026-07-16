
<!-- page 1 -->

**Supervisory Stress Test Model Documentation**

**Pre-Provision Net Revenue (PPNR) Model**

**October 2025**

**Updated December 2025**
<!-- page 2 -->

This document summarizes the pre-provision net revenue (PPNR) model that the Federal Reserve Board of Governors (Board) intends to use in the 2026 Supervisory Stress Test. The following sections provide a summary of the model, model components, and alternatives considered, along with other model-specific details. Documentation on the other models that the Board intends to use in the 2026 Supervisory Stress Test is available at the following link: https://www.federalreserve.gov/supervisionreg/dfa-stress-tests-2026.htm

<!-- Source PDF page 3 -->

## Table of Contents

- [A. Revisions](#sec-0)
- [B. Pre-Provision Net Revenue Model](#sec-1)
    - [i. Statement of Purpose](#sec-2)
    - [ii. Model Framework](#sec-3)
        - [a. Regression Models](#sec-4)
            - [(1) Justification for the Use of Regression Models](#sec-5)
            - [(2) General Specification of Regression Models](#sec-6)
            - [(3) Variables Used in Regression Models](#sec-7)
                - [(a) Dependent Variable and Scaling Balances](#sec-8)
                - [(b) Autoregressive Specification](#sec-9)
                - [(c) Macroeconomic Variable Selection](#sec-10)
            - [(4) Addressing Firm Heterogeneity: Firm Characteristics, Fixed Effects, and Grouping](#sec-11)
            - [(5) Calculation of Quarterly Projections from Regression Models](#sec-12)
            - [(6) Assumptions and Limitations of Regression Models](#sec-13)
        - [b. Structural Models](#sec-14)
            - [(1) Assumptions and Limitations of Structural Models](#sec-15)
        - [c. Nonparametric Models](#sec-16)
            - [(1) Method Description](#sec-17)
            - [(2) Assumptions and Limitations of Nonparametric Models](#sec-18)
        - [d. Data Sources and Treatment](#sec-19)
            - [(1) Pro Forma Adjustment Process](#sec-20)
            - [(2) Data Sources](#sec-21)
        - [e. Subordinated Debt Data Construction](#sec-22)
    - [iii. Questions](#sec-23)
    - [iv. Pre-Provision Net Revenue Model Components](#sec-24)
        - [a. Regression Models for Interest Income](#sec-25)
        - [b. Interest Income on Loans](#sec-26)
            - [(1) Description](#sec-27)
            - [(2) Model Specification](#sec-28)
            - [(3) Variable Selection](#sec-29)
            - [(4) Assumptions and Limitations](#sec-30)
            - [(5) Questions](#sec-31)
        - [c. Interest Income on Interest-Bearing Balances](#sec-32)
            - [(1) Description](#sec-33)
            - [(2) Model Specification](#sec-34)
            - [(3) Variable Selection](#sec-35)
            - [(4) Assumptions and Limitations](#sec-36)
            - [(5) Questions](#sec-37)
        - [d. Interest Income on U.S. Treasuries](#sec-38)
            - [(1) Description](#sec-39)
            - [(2) Model Specification](#sec-40)
            - [(3) Variable Selection](#sec-41)
            - [(4) Assumptions and Limitations](#sec-42)
            - [(5) Questions](#sec-43)
        - [e. Interest Income on Mortgage-Backed Securities](#sec-44)
            - [(1) Model Specification](#sec-45)
            - [(2) Variable Selection](#sec-46)
            - [(3) Assumptions and Limitations](#sec-47)
            - [(4) Questions](#sec-48)
        - [f. Interest Income on Other Securities](#sec-49)
            - [(1) Model Specification](#sec-50)
            - [(2) Variable Selection](#sec-51)
            - [(3) Assumptions and Limitations](#sec-52)
            - [(4) Questions](#sec-53)
        - [g. Interest Income from Trading Assets](#sec-54)
            - [(1) Model Specification](#sec-55)
            - [(2) Variable Selection](#sec-56)
            - [(3) Assumptions and Limitations](#sec-57)
            - [(4) Questions](#sec-58)
        - [h. All Other Interest Income](#sec-59)
            - [(1) Model Specification](#sec-60)
            - [(2) Variable Selection](#sec-61)
            - [(3) Assumptions and Limitations](#sec-62)
            - [(4) Questions](#sec-63)
        - [i. Regression Models for Interest Expense](#sec-64)
            - [(1) Interest Expense on Domestic Time Deposits](#sec-65)
                - [(a) Model Specification](#sec-66)
                - [(b) Variable Selection](#sec-67)
                - [(c) Assumptions and Limitations](#sec-68)
                - [(d) Questions](#sec-69)
            - [(2) Interest Expense on Other Domestic Deposits](#sec-70)
                - [(a) Model Specification](#sec-71)
                - [(b) Variable Selection](#sec-72)
                - [(c) Assumptions and Limitations](#sec-73)
                - [(d) Questions](#sec-74)
            - [(3) Interest Expense on Foreign Deposits](#sec-75)
                - [(a) Model Specification](#sec-76)
                - [(b) Variable Selection](#sec-77)
                - [(c) Assumptions and Limitations](#sec-78)
                - [(d) Questions](#sec-79)
            - [(4) Interest Expense on Trading Liabilities, Other Borrowed Money and All Other Interest Expense](#sec-80)
                - [(a) Model Specification](#sec-81)
                - [(b) Variable Selection](#sec-82)
                    - [Large Group](#sec-83)
                    - [Small Group](#sec-84)
                    - [Other Variables](#sec-85)
                - [(c) Assumptions and Limitations](#sec-86)
                - [(d) Questions](#sec-87)
        - [j. Regression Models for Noninterest Income](#sec-88)
            - [(1) Noninterest Income on Trading Revenue](#sec-89)
                - [(a) Model Specification](#sec-90)
                - [(b) Variable Selection](#sec-91)
                - [(c) Assumptions and Limitations](#sec-92)
                - [(d) Questions](#sec-93)
            - [(2) Noninterest Income on Service Charges on Deposits](#sec-94)
                - [(a) Model Specification](#sec-95)
                - [(b) Variable Selection](#sec-96)
                - [(c) Assumptions and Limitations](#sec-97)
                - [(d) Questions](#sec-98)
            - [(3) Noninterest Income from Net Servicing Fees](#sec-99)
                - [(a) Model Specification](#sec-100)
                - [(b) Variable Selection](#sec-101)
                - [(c) Assumptions and Limitations](#sec-102)
                - [(d) Questions](#sec-103)
            - [(4) Noninterest Income from Investment Banking Fees](#sec-104)
                - [(a) Model Specification](#sec-105)
                - [(b) Variable Selection](#sec-106)
                - [(c) Assumptions and Limitations](#sec-107)
                - [(d) Questions](#sec-108)
            - [(5) Noninterest Income from Fiduciary Income and Insurance Banking Fees](#sec-109)
                - [(a) Model Specification](#sec-110)
                - [(b) Variable Selection](#sec-111)
                - [(c) Assumptions and Limitations](#sec-112)
                - [(d) Questions](#sec-113)
        - [k. Regression Models for Noninterest Expense](#sec-114)
            - [(1) Noninterest Expense on Compensation](#sec-115)
                - [(a) Model Specification](#sec-116)
                - [(b) Variable Selection](#sec-117)
                - [(c) Adjustment for Variable Compensation](#sec-118)
                - [(d) Assumptions and Limitations](#sec-119)
                - [(e) Questions](#sec-120)
            - [(2) Noninterest Expense on Fixed Assets](#sec-121)
                - [(a) Model Specification](#sec-122)
                - [(b) Variable Selection](#sec-123)
                - [(c) Assumptions and Limitations](#sec-124)
                - [(d) Questions](#sec-125)
        - [l. Estimated Parameters of Regression Models](#sec-126)
        - [m. Structural Models](#sec-127)
            - [(1) Interest Income from Federal Funds Sold and Securities Purchased under Agreements to Resell](#sec-128)
                - [(a) Model Description](#sec-129)
                - [(b) Assumptions and Limitations](#sec-130)
                - [(c) Questions](#sec-131)
            - [(2) Interest Expense on Federal Funds Purchased and Securities Sold under the Agreements to Repurchase](#sec-132)
                - [(a) Model Description](#sec-133)
                - [(b) Assumptions and Limitations](#sec-134)
                - [(c) Questions](#sec-135)
            - [(3) Interest Expense on Subordinated Debt](#sec-136)
                - [(a) Model Description](#sec-137)
                - [(b) Assumptions and Limitations](#sec-138)
                - [(c) Questions](#sec-139)
        - [n. Nonparametric Models](#sec-140)
            - [(1) All Other Noninterest Income](#sec-141)
                - [(a) Model Description](#sec-142)
                - [(b) Questions](#sec-143)
            - [(2) All Other Noninterest Expense](#sec-144)
                - [(a) Model Description](#sec-145)
                - [(b) Assumptions and Limitations](#sec-146)
                - [(c) Questions](#sec-147)
    - [v. Proposed Models for 2026 Pre-Provision Net Revenue Components](#sec-148)
        - [a. Proposed Structural Models](#sec-149)
            - [(1) Interest Income on Loans](#sec-150)
                - [(a) Model Description](#sec-151)
                - [(b) Portfolio Segmentation](#sec-152)
                    - [Wholesale](#sec-153)
                    - [Corporate](#sec-154)
                    - [CRE](#sec-155)
                    - [Retail](#sec-156)
                    - [Mortgage](#sec-157)
                    - [Auto Loan](#sec-158)
                    - [Consumer and Small Business Credit Card](#sec-159)
                    - [Other Consumer Products](#sec-160)
                    - [Projected Interest Income Rate](#sec-161)
                    - [Variable-rate products](#sec-162)
                    - [Base rate assumptions](#sec-163)
                    - [Spread Estimation](#sec-164)
                    - [Fixed-Rate Products](#sec-165)
                    - [Industry Scalar](#sec-166)
                - [(c) Model Assumptions and Limitations](#sec-167)
                    - [Assumptions](#sec-168)
                    - [Limitations](#sec-169)
                    - [Retail Portfolio](#sec-170)
                    - [Wholesale Portfolio](#sec-171)
                - [(d) Questions](#sec-172)
            - [(2) Interest Income on Deposits with Banks and Other](#sec-173)
                - [(a) Model Description](#sec-174)
                - [(b) Assumptions and Limitations](#sec-175)
                - [(c) Questions](#sec-176)
            - [(3) Interest Income on U.S. Treasuries](#sec-177)
                - [(a) Model Specification](#sec-178)
                - [(b) Assumptions and Limitations](#sec-179)
                - [(c) Questions](#sec-180)
            - [(4) Interest Income on Mortgage-Backed Securities](#sec-181)
                - [(a) Model Specification](#sec-182)
                - [(b) Assumptions and Limitations](#sec-183)
                - [(c) Questions](#sec-184)
            - [(5) Interest Income on Other Securities](#sec-185)
                - [(a) Model Specification](#sec-186)
                - [(b) Assumptions and Limitations](#sec-187)
                - [(c) Questions](#sec-188)
            - [(6) Interest Income on Other Interest/Dividend-Bearing Assets](#sec-189)
                - [(a) Model Description](#sec-190)
                - [(b) Assumptions and Limitations](#sec-191)
                - [(c) Questions](#sec-192)
            - [(7) Interest Expense on Domestic Time Deposits](#sec-193)
                - [(a) Model Specification](#sec-194)
                - [(b) Assumptions and Limitations](#sec-195)
                - [(c) Questions](#sec-196)
            - [(8) Interest Expense on Other Domestic Deposits](#sec-197)
                - [(a) Model Specification](#sec-198)
                - [(b) Assumptions and Limitations](#sec-199)
                - [(c) Questions](#sec-200)
            - [(9) Interest Expense on Foreign Deposits](#sec-201)
                - [(a) Model Specification](#sec-202)
                - [(b) Assumptions and Limitations](#sec-203)
                - [(c) Questions](#sec-204)
            - [(10) Interest Expense on Federal Funds Purchased and Securities Sold under the Agreement to Repurchase](#sec-205)
                - [(a) Model Description](#sec-206)
                - [(b) Assumptions and Limitations](#sec-207)
                - [(c) Questions](#sec-208)
        - [b. Estimated Parameters for Proposed Structural Models](#sec-209)
        - [c. Proposed Adjustments to Pre-Provision Net Revenue Models to Incorporate the Impact of Interest Rate Risk Hedges](#sec-210)
            - [(1) Model Specification](#sec-211)
            - [(2) Assumptions and Limitations](#sec-212)
            - [(3) Questions](#sec-213)
        - [d. Proposed Regression Models](#sec-214)
            - [(1) Net Interest Income on Trading Assets and Liabilities](#sec-215)
                - [(a) Model Specification](#sec-216)
                - [(b) Variable Selection](#sec-217)
                - [(c) Assumptions and Limitations](#sec-218)
                - [(d) Questions](#sec-219)
            - [(2) Interest Expense on Other Borrowing](#sec-220)
                - [(a) Model Description](#sec-221)
                - [(b) Assumptions and Limitations](#sec-222)
                - [(c) Questions](#sec-223)
        - [e. Estimated Parameters for Proposed Regression Models](#sec-224)
        - [f. Proposed Noninterest Income and Expense Models Using Firm Projections](#sec-225)
            - [(1) Noninterest Income](#sec-226)
                - [(a) Model Specification](#sec-227)
                - [(b) Variable Selection](#sec-228)
                - [(c) Assumptions and Limitations](#sec-229)
                - [(d) Questions](#sec-230)
            - [(2) Noninterest Expense Model Using the Efficiency Ratio Projections](#sec-231)
                - [(a) Model Description](#sec-232)
                - [(b) Assumptions and Limitations](#sec-233)
                - [(c) Questions](#sec-234)
        - [g. Estimated Parameters for Proposed Noninterest Income and Expense Models Using Firm Projections](#sec-235)

<!-- page 4 -->

<!-- Source PDF page 4 -->

<a id="sec-0"></a>

# A. Revisions

The Federal Reserve revised this documentation in December 2025, to reflect additional parameters for the proposed suite of pre-provision net revenue models for the 2026 stress test, as well as to make other technical corrections. The revisions are listed below:

On pages 168-169, a paragraph was added at the bottom of page 168 that summarizes the four model types for the Board’s proposed suite of pre-provision net revenue models. Additionally, Table A6 was added to clearly delineate the pre-provision net revenue components by these model types.

On page 175, in the paragraph under “Wholesale,” extraneous symbols in the first and second sentences were removed. Additionally, in the first sentence, the word “two” was revised to “two parts” and a colon was added for clarity. Additionally, the terms “category” and “loan type” were pluralized in the first sentence in the first paragraph under “Corporate”.

On page 180, in the paragraph under “Projected Interest Income Rate,” a period was added to the end of the second sentence.

On page 209, in the last sentence of the first paragraph under “(7) Interest Expense on Domestic Time Deposits,” the term “end of quarter” was revised to “average.”

On page 214, in the first sentence, the term “end of quarter” was revised to “average” and the term “FR Y-9C” was revised to “FR Y-14Q.” Additionally, the label for the subsection “Assumptions and Limitations” was changed from (a.) to (b), and in the last paragraph under “(b) Assumptions and Limitations,” the word “contradicts” was revised to “abstracts from.”

On page 215, the label for the subsection “Questions” was changed from (b) to (c).

On page 216, in the last sentence, the term “federal funds sold” was revised to “federal funds purchased.”

On pages 219-220, a section titled “Estimated Parameters for Proposed Structural Models” was added.

On page 234, a section titled “Estimated Parameters for Proposed Regression Models” was added.

On page 237, in the second sentence of the second to last paragraph, the term “asset servicing” was revised to “investment servicing” and a comma was added for clarity.

On pages 240 and 243, Equations A56, A57, and A64 were revised to state that $URQ(E,t)$ is the quarterly change in the unemployment rate in exercise *E* “at” projection quarter *t*, as opposed to “from Q0 to” projection quarter *t*.

On page 243, Equation A64 was revised to state that *Treasury10y* is the quarterly change in the 10-year Treasury yield in exercise *E* “at” projection quarter *t*, as opposed to “from Q0 to” projection quarter *t*.
<!-- page 5 -->

On pages 251-255, a section titled “Estimated Parameters for Proposed Noninterest Income and Expense Models Using Firm Projections” was added.
<!-- page 6 -->

<!-- Source PDF page 6 -->

<a id="sec-1"></a>

# B. Pre-Provision Net Revenue Model

The Board is proposing to use a new suite of models to project pre-provision net revenue in the 2026 stress test. The proposed suite of models is discussed in Section A.v. The current suite of models (i.e., those used in the 2025 stress test) are described in Sections A.i-A.iv. The Board seeks public input on both the current and the proposed suites of models.

While the current regression models based on historical data have in general demonstrated good forecasting performance across time, they are subject to certain limitations in capturing the business practices that generate pre-provision net revenue. The proposed models aim to better capture business practices by using granular position data to model net interest income and bank projections to model noninterest income and expense.

The Board requests public input on (i) using the 2025 models in 2026; (ii) using the proposed models in 2026; and (iii) whether there are other approaches the Board should consider for 2026.

<!-- Source PDF page 6 -->

<a id="sec-2"></a>

## i. Statement of Purpose

The Board estimates the effect of supervisory scenarios on firms participating in the stress test by projecting net income and other components of regulatory capital for each firm over the nine-quarter projection horizon. A key component of net income is pre-provision net revenue, which is defined as income from banking services, activities, and products, net of expenses related to the provision of these same services, activities, and products, excluding loan loss provisions. The components of pre-provision net revenue are net interest income (interest income minus interest expense), noninterest income, and noninterest expense, as provided in the equation below.
<!-- page 7 -->

**Equation A1** – Components of Pre-Provision Net Revenue

*Pre-Provision Net Revenue = Interest Income – Interest Expense + Non-Interest Income – Non-*

*Interest Expense*

The Board projects components of pre-provision net revenue using a suite of models that relate specific revenue and expense components to firm characteristics and macroeconomic variables. This suite of models is designed to project these components under the macroeconomic scenarios of the supervisory stress test. The models exclude components of pre-provision net revenue that are either capital neutral or modeled elsewhere in the supervisory stress test.[^1]

Revenue and expense components projected by the models generally vary based on changes in economic conditions over the nine quarters of the projection horizon. Those conditions are described in the models by interest rates, stock market returns and volatility, corporate bond spreads, and gross domestic product growth.

The Board separately models 23 components of pre-provision net revenue, which correspond to the terms in Equation A1 and are described below.[^2]
<!-- page 8 -->

- **Interest Income.** The Board models eight components of interest income: interest income on (1) federal funds and repurchase agreements, (2) interest-bearing balances, (3)

loans, (4) mortgage-backed securities, (5) other securities, (6) trading assets, (7) U.S.

Treasuries, and (8) all other interest income.

- **Interest Expense.** The Board models six components of interest expense: interest expense on (9) domestic time deposits, (10) federal funds and repurchase agreements,

(11) foreign deposits, (12) other domestic deposits, (13) subordinated debt, and (14)

trading liabilities, other borrowed money, and all other interest expenses.

- **Noninterest Income.** The Board models six components of noninterest income— (15) trading revenue and five components of noninterest, nontrading income:

(16) fiduciary income and insurance and banking fees, (17) investment banking fees, (18)

net servicing fees, (19) service charges on deposits, and (20) all other noninterest income.

- **Noninterest Expense.** The Board models three components of noninterest expense: (21) compensation expense, (22) fixed asset expense, and (23) all other noninterest

expense, excluding losses from operational-risk events and other real estate owned

expenses.

The Board has determined that the selection of 23 pre-provision net revenue components is appropriate based on data availability and overall model performance. This level of granularity is also consistent with the principles of robustness and stability from the Policy Statement as it facilitates the identification of underlying risks to income and expense streams that could be amplified during periods of economic stress. Further, the level of granularity aligns with the principles of consistency, comparability, and simplicity, as modeled components can be directly mapped to the FR Y-9C regulatory reporting form, a standardized supervisory reporting tool. The rationale for specific modeling choices is discussed in detail below.

<!-- Source PDF page 8 -->

<a id="sec-3"></a>

## ii. Model Framework

In designing models that project pre-provision net revenue components in the supervisory stress test, the Board considers the economic factors driving each component, as well as statistical properties of the individual income or expense component, data availability, and how
<!-- page 9 -->

component behavior varies across firms (i.e., heterogeneity). The Board uses four types of models to project the components of pre-provision net revenue:

- panel regression and autoregressive models that relate the components of a firm’s revenues and non-provision-related expenses, expressed as a share of the relevant asset or

liability balance, to macroeconomic variables, recent values of the revenue or expense

ratio, firm characteristics, and other independent variables;

- structural models that use granular data on individual positions to reflect a clear, pre-determined relationship to a macroeconomic variable in the stress scenario, or a simple

calculator approach based on clear assumptions; and

- simple nonparametric models that rely on recent firm-level performance. In determining which type of model is most appropriate to project each component, the Board balances the principles outlined in the Policy Statement. Table A1 presents the models applied to each component of pre-provision net revenue. Each model type is described in more detail below.

**Table A1** - Pre-Provision Net Revenue Components Model Specification Summary

| PPNR component | Normalized by | Model type | Regressors | Seasonality | Fixed effects | Firm groups |
|---|---|---|---|---|---|---|
| **Interest income component** | | | | | | |
| Loans | Total loans | Regression with year AR | Credit card loans / total loans (%), lag of term spread in percent (T10Y-T3M), 3-month Treasury yield | No | Yes | No |
| Interest-bearing balances | Interest-bearing balances | Regression with year AR | 3-month Treasury yield, lag of term spread in percent (T10Y-T3M) | No | Yes | No |
| U.S. Treasuries | U.S. Treasuries | Regression with year AR | Term spread in percent (T5Y-T3M), 3-month Treasury yield | No | Yes | No |
| Mortgage-backed securities | Mortgage-backed securities | Regression with year AR | Lag of 3-month Treasury yield | No | Yes | No |
| Other securities | Other securities | Regression | Term spread in percent (T10Y-T3M), 3-month Treasury yield, spread of BBB Bond Index to 10-year Treasury yield in percent | No | Yes | No |
| Federal funds sold and securities purchased under agreements to resell | n/a | Structural model / calculator | n/a | n/a | n/a | No |
| Trading assets | Trading assets | Regression with year AR | 3-month Treasury yield, spread of BBB Bond Index to 10-year Treasury yield | No | Yes | No |
| All other | Interest-earning assets | Regression with year AR | None | No | Yes | No |
| **Interest expense component** | | | | | | |
| Domestic time deposits | Total domestic time deposits | Regression with year AR | 3-month Treasury yield | No | Yes | No |
| Foreign deposits | Total foreign deposits | Regression with year AR | 3-month Treasury yield | No | Yes | No |
| Other domestic deposits | Other domestic deposits | Regression with year AR | 3-month Treasury yield | No | Yes | No |
| Federal funds purchased and securities sold under agreements to repurchase | n/a | Structural model / calculator | n/a | n/a | n/a | No |
| Trading liabilities, other borrowed money, and all other (large group) | Trading liabilities and other borrowed money | Regression with year AR | US Market Volatility Index, US Market Volatility Index ^2, 3-month Treasury yield | No | Yes | Yes, large and small |
| Trading liabilities, other borrowed money, and all other (small group) | Trading liabilities and other borrowed money | Regression with year AR | Unemployment rate, 3-month Treasury yield | No | Yes | Yes, large and small |
| Subordinated debt | n/a | Structural model / calculator | n/a | n/a | n/a | No |
| **Noninterest income component** | | | | | | |
| Service charges on deposits | Domestic deposits | Regression with year AR | 3-month Treasury yield | Yes | Yes | No |
| Investment banking fees (large group) | Total assets | Regression with year AR | Year over year change in VIX, change in spread of BBB bond index to 10-year Treasury yield in percent | Yes | Yes | Yes, large and small |
| Investment banking fees (small group) | Total assets | Regression with year AR | Change in spread of BBB bond index to 10-year Treasury yield in percent | No | Yes | Yes, large and small |
| Fiduciary income and insurance and banking fees | Total assets less trading assets | Regression with year AR | Year over year change in VIX | Yes | Yes | No |
| Net servicing fees | Total servicing assets | Regression | Annualized quarterly real GDP percent change | No | Yes | No |
| Trading revenue (large group, fixed income) | Trading assets | Regression with year AR | Change in BBB spread to (1+lag of BBB spread) | Yes | Yes | Yes, large and small |
| Trading revenue (large group, non-fixed income) | Trading assets | Regression with year AR | None | Yes | Yes | Yes, large and small |
| Trading revenue (small group) | Trading assets | Regression | 3-month Treasury yield | Yes | Yes | Yes, large and small |
| All other | Total assets | Median model | n/a | n/a | n/a | No |
| **Noninterest expense component** | | | | | | |
| Compensation (large group) | Total assets | Regression with year AR | Change in spread of BBB Bond Index to 10-year Treasury yield in percent | Yes | Yes | Yes, large and small |
| Compensation (small group) | Total assets | Regression with year AR | Change in spread of BBB Bond Index to 10-year Treasury yield in percent | No | Yes | Yes, large and small |
| Fixed assets | Total assets | Regression with year AR | None | Yes | Yes | No |
| All other | Total assets | Median model | n/a | n/a | n/a | No |

<!-- page 10 -->

<!-- page 11 -->

Notes: Items are sourced from FR Y-9C and FR Y-14. n/a stands for “not applicable.”

The Board uses a top-down approach to modeling pre-provision net revenue. This approach is informed by the work of Hirtle, Kovner, Vickery and Bhanot (2016),[^3] which shows that a simple top-down framework can be used to compute projections of bank capital and net income in response to macroeconomic scenarios. A top-down approach typically uses data series of income and expense components at the firm level, in contrast to more granular bottom-up approaches that can be based on detailed transaction level microdata. For instance, individual firms may use individual positions on their trading book to model trading revenue, whereas the Board models trading revenue on aggregate for each firm.

Hirtle, Kovner, Vickery and Bhanot (2016) applied regression models to forecast six pre-provision net revenue categories: net interest income, noninterest nontrading income, trading income, noninterest expense on compensation, noninterest expense on fixed assets, and other noninterest expense. Their specification used macroeconomic variables as independent variables and highlighted that components of pre-provision net revenue are highly correlated over time. In
<!-- page 12 -->

particular, the observed value of a component in a certain quarter is highly correlated with the observed value for the same component in the previous quarter. This type of correlation is commonly denominated in statistical literature as autoregressive.

Consistent with their work, most of the Board’s pre-provision net revenue component models are panel regression models that use an econometric approach to project pre-provision net revenue under stress.[^4] Econometric approaches enable the models to consider the economic drivers and statistical patterns of firm revenues and expenses using historical data to approximate how these same components may evolve in response to hypothetical events. This is because regression models can leverage high-quality, time-series data from the FR Y-9C reports starting in the year 1991 up to the present day.

However, for some pre-provision net revenue components, the Board has determined that a regression model is not appropriate. In these cases, the Board forecasts components using structural models or nonparametric models. These component models are explained in more detail below.

<!-- Source PDF page 12 -->

<a id="sec-4"></a>

### a. Regression Models

A regression model is a statistical method that estimates a relationship between a dependent (or outcome) variable and one or more independent (or input) variables. The sensitivity of the
<!-- page 13 -->

relationship between an independent variable and the dependent variable is represented by a model coefficient, which the Board estimates and uses to forecast results for a given macroeconomic scenario.

<!-- Source PDF page 13 -->

<a id="sec-5"></a>

#### (1) Justification for the Use of Regression Models

The Board primarily uses panel regression models to project pre-provision net revenue components for the following reasons. First, panel regression models use aggregate firm-level data that is readily available from the FR Y-9C. The FR Y-9C is a public data source that is well-known among industry, regulators, examiners, and the banking empirical research community. The FR Y-9C data has been available since 1986 and provides standardized and consistent data input across firms.

It is particularly important for regression models to use data that covers a large time period. Statistical models tend to be more comprehensive when they consider a large number of observations that include historical periods with diverse economic conditions to identify macroeconomic relationships. The Board’s pre-provision net revenue regression models thus rely on data from the FR Y-9C, which provides over 35 years’ worth of data. This long data history enables the regression models to leverage information from a variety of economic and financial cycles[^5] and reduces the weight of transitory factors or events on model results, consistent with the Policy Statement principle of robustness and stability.

Second, regression models are relatively simple compared to other econometric or statistical alternatives. Panel regressions are one of the most common and well-known methods of statistical analysis and forecasting among researchers and quantitative analysts. They are
<!-- page 14 -->

relatively simple to estimate, implement, and explain to an external audience. Furthermore, regression models allow for a more easily interpretable relationship between variables. Together, these factors support the choice of this method, in accordance with the Policy Statement principle of simplicity.

Third, when developing regression models for pre-provision net revenue components, the Board usually looks for statistically and economically significant responses to macroeconomic factors by testing each model against recessions or crisis periods. When such testing results are satisfactory, the Board considers that component to be appropriately modeled by the regression method, consistent with the Policy Statement’s emphasis on a model’s ability to capture the effect of economic stress.

Lastly, the panel regression models used by the Board to project pre-provision net revenue components are estimated and projected at the firm level on a quarterly basis. The Board chose this level of granularity and frequency as it provides good out-of-sample performance and standardized coefficients across banks, supported by the Policy Statement principle of consistency and comparability across firms. Panel regressions also provide flexibility to address heterogeneity in bank performance and to incorporate bank-level characteristics as independent variables. Addressing heterogeneity is an important issue for stress testing given that firms subject to the test operate with a variety of business models. Some firms mostly engage in typical banking activities of deposit taking and lending, while others are focused on trading, investment banking, or trust activities. Failing to recognize heterogeneity could jeopardize the forecasting ability of the models.

Alternative approaches to the panel regression model are industry-level regressions or separate regressions for individual banks. Industry-level regressions require further assumptions
<!-- page 15 -->

to address heterogeneity in firm performance, which can lead to increased variance in projections over stress testing cycles. For example, the use of market-share criteria could be an option to map an industry-level projection to bank-specific forecasts, but since market share tends to vary a lot over time this could generate increased volatility in stressed projections over cycles. On the other hand, separate regressions for individual banks do not provide standardized coefficients for all banks, but one projection equation for each firm. Given that each equation would be estimated with much fewer observations, this approach would result in increased variance in coefficients and model projections over stress testing cycles, especially for banks with shorter time series of data available. In addition, the use of individual models for each firm would be in conflict with the Policy Statement principle of comparability.

<!-- Source PDF page 15 -->

<a id="sec-6"></a>

#### (2) General Specification of Regression Models

The panel regression models are generally specified according to the following equation:

**Equation A2** – Panel Regression Models General Specification

$$Ratio(b,t) = f\left(\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4},\ FE(b),\ FE(b) * Ind(T-Q < t \le T),\ Z(t),\ X(b,t)\right),$$

*where:*

- $b$ represents the firm;
- $t$ represents time (year-quarter);
- $Ratio(b,t)$ represents the ratio of the component to a scaling balance (for more information on component ratios and scaling balances, see the next section on Variables used in Regression Models and Table A1 above);
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ represents the autoregressive term, defined as the mean of the component ratio over the past four quarters and where $j$ is the lagged quarter;
- $FE(b)$ represents the fixed effect for firm $b$;
- $FE(b) * Ind(T-Q < t \le T)$ represents the trailing multiyear fixed effect (rolling-window fixed effect) for the last $Q$ quarters for firm $b$, where $T$ is the end of the estimation period;
- $Z(t)$ represents one or more of the macroeconomic variables from the stress test scenario; and

<!-- page 16 -->

- $X(b,t)$ includes firm characteristics and other controls, such as seasonal factors in some specifications.

The next subsection describes each element of the regression models in more detail.

<!-- Source PDF page 16 -->

<a id="sec-7"></a>

#### (3) Variables Used in Regression Models

<!-- Source PDF page 16 -->

<a id="sec-8"></a>

##### (a) Dependent Variable and Scaling Balances

The dependent variable of the regression for each pre-provision net revenue component is defined as a ratio of the respective income or expense component divided by the corresponding balance sheet asset or liability level (see Table A1 for more detail on scaling balances). Both the denominator and the numerator are in dollars measured at each quarter-end. The ratio format follows naturally from the model by Hirtle, Kovner, Vickery and Bhanot (2016). When calculating projections for components of pre-provision net revenue, the projected component ratios are multiplied by the corresponding scaling balances to arrive at projections in dollar amounts.

Using a ratio instead of the gross dollar income or expense flow is a practical way to account for differences in the size of banks in the sample. In addition, this approach almost always guarantees stationarity of the time series which is an important requirement from the statistical standpoint. As is well recognized in statistics, a regression model with a nonstationary dependent variable is subject to spurious correlation (in case any of the independent variables are also nonstationary) and can also lead to forecasts which are explosive in nature.

<!-- Source PDF page 16 -->

<a id="sec-9"></a>

##### (b) Autoregressive Specification

Most of the regression models used to model pre-provision net revenue components include an autoregressive term. An autoregressive term reflects the recent past performance of the dependent variable. For example, in a regression of the ratio of interest income on loans to
<!-- page 17 -->

total loans, the autoregressive term is the average of that ratio over the previous four quarters. Autoregressive terms are usually included in time series models when past performance is informative in predicting future outcomes. For the pre-provision net revenue component models with an autoregressive term, it has been shown that these autoregressive terms improve model forecast performance as they contain useful information about the expected trajectory of the dependent variable.

In the Board’s implementation, the autoregressive term is defined as the mean of the dependent variable over the previous four quarters (the Year AR term, as shown in Table A1). Using an autoregressive term calculated over the past four quarters as opposed to a single quarter reduces volatility driven by changes across individual quarters, such as seasonal effects related to winter holidays, and improves model performance.[^6] Therefore, this approach is consistent with the Policy Statement principle of robustness and stability.

The Board uses a statistical procedure to determine the benefits of including an autoregressive term. Specifically, the Board compares regression models with and without the inclusion of the autoregressive term using the Bayesian Information Criterion.[^7] In its evaluation,
<!-- page 18 -->

the Board includes bank, time (quarter-year), and post-2008 financial crisis fixed effects (an indicator taking the value of one after 2009:Q1 until the end of the sample) in the regressions and clusters the residuals using the time variable. The Board estimates two models using the same estimation sample: with a Year AR and without. Among these models, the Board selects the model with the minimum Bayesian Information Criterion. If there is a difference of less than or equal to 5% in the Bayesian Information Criteria, the Board selects the model without an autoregressive term. As Table A1 indicates, most regression models benefit from the inclusion of the Year AR term.

<!-- Source PDF page 18 -->

<a id="sec-10"></a>

##### (c) Macroeconomic Variable Selection

The Board typically adopts one or more macroeconomic variables included in the supervisory stress test scenarios as independent variables for each regression model. The macroeconomic variables are selected based on their statistical significance and consistency with the expected economic relation with the dependent variable being projected. For example, if a certain income component is expected (from the economic standpoint) to be positively related to the short-term interest rate, we should expect that the regression outcome indicates a positive coefficient for the independent variable that represents the short-term rate.

The Board follows a process to choose macroeconomic variables with the strongest correlation with the corresponding regression dependent variable, and therefore the best indicative power. Where possible, the selection is based on and is consistent with previous findings from academic literature on bank performance and its sensitivity to macroeconomic factors.[^8] Furthermore, to limit the potential for pre-testing bias or the introduction of spurious
<!-- page 19 -->

relationships, the Board initially selects variables for each component based on well-established economic relationships. In this context, well-established economic relationships are considered those usually discussed in standard textbooks adopted in undergraduate courses in financial markets and banking.[^9]

For example, yields on U.S. Treasury securities are key variables in the models of interest income and expense components because those securities serve as base rates for many types of floating-rate loans and as alternative investments for holders of bank liabilities. Real GDP growth, stock market returns, and credit spreads are included in some of the Board models of the noninterest income and noninterest expense components. In general, interest income and expense model components include interest rate variables, and noninterest income and expense model components include variables that measure financial market distress or overall economic activity.

Selection factors for macroeconomic variables include: (i) whether the sign (positive or negative) of the coefficient on the variable in the model is consistent with the conceptually expected relationship; (ii) how well the model performs when incorporating new data (out-of-

relationship between the federal funds rate and the term spread by examining the relationship between stock returns and the surprise component of changes in interest rates. Demirguc-Kunt and Huizinga (1999) found that net interest margin is positively associated with bank characteristics such as the share of loans and deposits. They also found that net interest margin is related to real interest rates and inflation rates but could not confirm a relationship between net interest margins and gross domestic product growth. See Flannery, M.J. and James, C.M., 1984. The
<!-- page 20 -->

sample forecasting performance); (iii) the variable’s impact on the stability of the model (e.g., how much the macroeconomic variables affect the estimated coefficients of other independent variables of the model over time); and (iv) the macroeconomic sensitivity of the results. In this context, macroeconomic sensitivity of results refers to the ability of the dependent variable of the model to respond, in an economically significant way, to large changes in the independent macroeconomic variable during a forecasting exercise.

Macroeconomic variables can enter the regressions either at their original values or following mathematical transformations (for example, in first difference, percentage change, or change in the natural logarithm). Transformations are useful because some dependent variables may present a stronger statistical response to a transformation than to the original measure of a macroeconomic variable. For instance, it may be the case that empirically some types of bank fee income are more responsive to changes in credit spreads than to the current level of the credit spread. To reduce complexity, the Board utilizes the Bayesian Information Criterion to identify the simplest regression model specification and its corresponding macroeconomic variables and their transformations (see details below). The macroeconomic variables selected for each regression model are listed Table A1.

Once the Board identifies a set of economic variables of interest, the Board estimates three sets of models:

- First, the Board constructs a “benchmark” regression model with no macroeconomic variables, adding fixed effects and choosing the autoregressive term based on the

standard process (described in the previous subsection). In this context, fixed effects

consist of a group of independent variables that enter the regression model. Each of these

independent variables represents one firm. The independent variable will have a value of

one for the firm it represents, and zero for all other cases.

- Next, the Board adds a set of intuitive macroeconomic variables to the benchmark model, keeping the variables that produce statistically significant coefficient estimates. The
<!-- page 21 -->

resulting “intuitive” model has a selected autoregressive structure, fixed effects, and

significant intuitive macroeconomic variables.

- Finally, the Board considers the full set of all macroeconomic variables and their transformations and adds them one-by-one to the previous intuitive model.[^10] The Board

chooses ten variables with the lowest Bayesian Information Criterion among the

significant macroeconomic variables and transformations. The ten-variable limit is an

upper bound to avoid a saturated model (a model with too many independent variables).

This is defined as the “extended” model.[^11]

Based on these three models (benchmark, intuitive, and extended), the Board evaluates a series of additional model specifications using a stepwise regression procedure. Stepwise regression is a method for selecting a subset of independent variables in a regression model by systematically adding or removing variables based on statistical significance or other previously defined criteria. The Board uses a stepwise regression procedure that evaluates model specifications incorporating the variables selected through the previous steps with combinations of three macroeconomic variables. The choice of the maximum of three macroeconomic variables aims to limit model complexity and to achieve a relatively concise final specification. Calendar quarter seasonality indicator variables are also incorporated into component regression models, where applicable, to reduce the impact associated with recurring seasonal trends.[^12]
<!-- page 22 -->

In choosing macroeconomic variables and the underlying model final specification, the Board focuses on out-of-sample model performance, stability, and macroeconomic sensitivity. The Board applies the following general principles:

- Out-of-sample performance (OOS): Since stepwise regression is prone to in-sample overfitting, the Board selects additional variables only if they contribute to a reduction in

the out-of-sample nine-quarter ahead root-mean square error (RMSE) of more than

0.05.[^13],[^14] In this context, the root-mean square error (RMSE) is calculated using the standard formula as $RMSE = \sqrt{(\sum(\hat{y}_i - y_i)^2)/n}$, where $\hat{y}_i$ is the predicted value, $y_i$ is the observed value, and $n$ is the number of observations predicted. In order to compare the model with the additional variables to the current specification, the Board calculates the ratio of the root-mean square errors of each model (candidate model divided by the current model). If the value of this ratio is 0.95 or less, it is understood that the candidate

model reduces root-mean square error by more than 0.05, or 5%.

- Stability: Adding correlated explanatory variables in a stepwise regression may result in model instability, which occurs when estimated coefficients on other independent

variables change over time. The Board selects additional variables in the stepwise

regression only if they do not increase the standard deviation of the nine-quarter out-of-

sample bank-level prediction for a certain sample of interest. To assess this, the model is

re-estimated quarterly for the starting points from 2010:Q2 to 2018:Q4. The standard

deviation of the out-of-sample prediction is used at this step as a proxy to measure model

instability.

- Macroeconomic sensitivity: Lastly, the Board compares forecasts in the severely adverse versus the baseline scenarios from several previous stress testing cycles and chooses

models with greater macroeconomic sensitivity, all else equal. This reflects the principle

of conservatism and ensures the final model can capture effects of economic stress.
<!-- page 23 -->

<!-- Source PDF page 23 -->

<a id="sec-11"></a>

#### (4) Addressing Firm Heterogeneity: Firm Characteristics, Fixed Effects, and Grouping

The firms subject to the supervisory stress test employ a wide array of business models. Some firms focus on lending to particular segments (e.g., credit card lending), while others may engage in diverse operations, such as trading activities or asset custody. The heterogeneity in business models can impair the effectiveness of regression models for forecasting, if a dependent variable (income or expense flow) for some firms consistently behaves differently than for other firms in the sample.

The reasons for heterogeneous behavior of the dependent variable for certain firms can be related to at least two possible characteristics. First, firms can have different average levels of the dependent variable (income or expense flow) over time, independently of the point in the business cycle. For instance, if the ratio of interest income on loans is consistently higher for credit-card-oriented firms than for other firms, then the forecast produced by a simple model (with no firm fixed effects) will under-report their earnings. Second, dependent variables for some firms (income or expense flows) can have different sensitivities to macroeconomic independent variables. For example, if compensation expenses for some firms are more sensitive to macroeconomic conditions, then a simple model (with just one group of firms) may not capture the variability in compensation expense in response to business cycle conditions. The Board has taken several steps to address these types of heterogeneity.

First, to address cases in which the average level of the dependent variable differs across firms over time, the Board looks for firm characteristics that could be correlated to the observed heterogeneity. For example, the loan portfolio mix can be correlated with the average level of the interest income on loans ratio and there could be substantial variability across firms on that
<!-- page 24 -->

ratio. If the data on firm characteristics is available, then the Board considers including additional variables related to that feature in certain component regression models. In many cases, these additional variables are intended to account for material differences across firms that may change the level of the component across banks and over time. The Board chooses a set of available variables based on the Board’s experience and expertise and evaluates model performance and prioritizes concise models as discussed in the previous subsection.

Second, even in cases in which firm level variables are added to capture heterogeneity across firms, which varies over time, panel regression models typically need to address the impact of general heterogeneity in the cross section of firms on the long-run average level of the dependent variable. One standard approach, which has been adopted by the Board, is to include firm-specific fixed effects as independent variables in each regression.

Firm-specific fixed effects allow the projected average of the dependent variable (i.e., revenues) to vary depending on the firm. The inclusion of fixed effects ensures that projections converge to a firm’s average level (i.e., revert to the firm-specific mean) if macroeconomic conditions are unchanged. For example, if a firm has higher expenses than its peers on average, the firm-specific fixed effect will reflect this fact in the projections.

Fixed effects capture unobserved heterogeneity in each firm’s revenue generation process (e.g., market power, business strategy, and asset and liability duration) and are often economically significant and generally statistically significant. As a result of fixed effects, the Board’s component projections converge over time toward the firm’s recent average performance in the corresponding revenue or expense component, while still allowing for variation in response to changes in macroeconomic conditions.
<!-- page 25 -->

Third, to better capture changes in the average performance of each firm over the more recent period, the Board includes rolling-window (trailing) firm-specific fixed effects in the specification of all regression models. The rolling-window period is defined as the last seven years starting at (and including) the quarter in which the projections begin (typically the last quarter of the year). The rolling-window fixed effect variable is a firm-specific variable which interacts (multiplies) a firm-specific fixed effect with an indicator variable that takes the value of one for the past seven years and for the projection horizon and zero for the rest of the estimation sample. The seven-year rolling-window fixed effects allow the projection for a firm to revert to its recent mean, conditional on other variables.

The period of seven years for the rolling-window fixed-effects was chosen based on projection stability and forecasting performance. The Board evaluated other potential lengths for the rolling window (between 3 and 7 years) and found that shorter windows did not improve model out-of-sample performance and stability for most cases. The 7-year rolling window typically improved model forecasting ability and reduced the out-of-sample forecast errors when compared with alternative choices of period lengths. Periods longer than seven years were not found to improve forecasting performance for most components. In any case, for firms without long histories of FR Y-9C data, periods larger than seven years for the rolling-window would be highly correlated with the firm fixed-effects, adding little explanatory power and increasing model parameter variance.

Fourth, the model also includes a set of fixed effects that capture major firm-specific events. For instance, a firm could experience a significant merger event at some point in the estimation period, which the pro forma adjustment data construction process cannot properly account for due to a lack of data availability on the past outcomes of the acquired firm. In such
<!-- page 26 -->

cases, a variable is added to the regression taking the value of one for the first period (pre-merger), only for the affected firm, and zero forward. The standard firm fixed effect variable remains in the regression for each firm, where the value is one for the whole period. The presence of the firm-break variables allows the regression model to account for different dependent variable averages before and after the merger event. The Board uses a similar approach for significant accounting changes that affect a single component of pre-provision net revenue.

Next, to address differences across banks in the sensitivity of the income or expense component to macroeconomic conditions, in some specific cases, the Board estimates different regressions by groups of firms. Groups are determined in cases where there are clearly wide differences across banks in the share of the income (or expense) component relative to total income (or expense), and where heterogeneity has been observed historically. For example, interest expense on trading liabilities, other borrowed money, and all other typically accounts for a large share of total interest expense (around 30 percent) for some types of firms (notably the larger firms), while representing a small share for others (around 5 percent for smaller firms). This component is therefore modeled using two groups, and different regressions are estimated for each group.

During the model development process, the Board typically evaluates the possibility of using groups for each component of pre-provision net revenue. The Board considers a combination of firm type (business model) and size to determine candidate groups. Banks are classified into two different groups, large and small, based on their concentration and on the correlation of the dependent variable with other peer firms. The Board generally selects a maximum of two groups for simplicity, but under some circumstances, the Board may consider
<!-- page 27 -->

models containing up to three groups. The Board then selects to model a component either in aggregate or in groups based on out-of-sample model forecast performance.[^15]

Finally, the Board assumes that firms with greater relative activity in a particular income or expense component should have more influence over the regression coefficients for that component. This assumption also implies that firms that are not particularly active in a given business line should not unduly affect model coefficients for the component representing this line. To implement this assumption, the Board uses a weighted least squares estimation procedure for all regressions. This choice prevents the behavior of firms with little activity in a given business line from exerting too much influence over coefficients in the regression. The regression weights are defined as the value of the firm-specific scaling balance for the dependent variable (the balance used to compute the ratio of a given income or expense component) divided by the total balance for all firms in the model. This approach is conceptually similar to accounting for firms’ market shares in a given business line.

<!-- Source PDF page 27 -->

<a id="sec-12"></a>

#### (5) Calculation of Quarterly Projections from Regression Models

To calculate quarterly projections for each firm, the Board uses a standard panel regression procedure for conditional forecasting. For all firms, every quarter-ahead projection for the ratio of the component is calculated one quarter at a time, using the estimated regression coefficients and the regression independent variables. If the autoregressive term is present, then it must be recalculated at each step-ahead using the forecasted quantity of the previous step (except at lift-off where observed data for the dependent variable is used as input to the autoregressive term). Next, the Board multiplies all the ratios projected by their correspondent
<!-- page 28 -->

scaling balances (typically an asset or liability balance quantity) to convert them into projected dollar amounts.

Using the notation from Equation A2, the process is as follows:

- For the first quarter of projection $t+1$, the Board forecasts the component ratio $\widehat{Ratio}(b,t+1)$ from Equation A2 for all firms, conditional on firm observed data $X(b,t)$, macroeconomic variables $Z(t)$, and the autoregressive term (if present) $\sum_{j=0}^{j=3}\frac{Ratio(b,t-j)}{4}$;
- For the second quarter of projection $t+2$, the Board first recalculates the autoregressive term (if present) now denominated $\sum_{j=0}^{j=3}\frac{\widehat{Ratio}(b,t+1-j)}{4}$, then forecasts $\widehat{Ratio}(b,t+2)$, conditional on $X(b,t+1)$, $Z(t+1)$, and on the new autoregressive term;
- For the remaining quarters, the Board sequentially reapplies the procedure of quarter $t+2$ to calculate component ratio projections for the whole horizon; and
- Ratio projections are multiplied by the corresponding balances for the component to generate dollar-amount projections.

Additionally, the Board sets a lower bound of zero for the ratio projections of certain components. Even under the adverse economic conditions contemplated in the severely adverse scenario, the Board considers that projections for some components are unlikely to be negative and thus sets a zero lower bound for these cases. Furthermore, projections may be set to zero or statistically equal to zero if a firm recently exited a business line and therefore has no activity in a given component for the four quarters prior to the projected quarter. These lower bound specifications promote consistency and stability in the model results.

<!-- Source PDF page 28 -->

<a id="sec-13"></a>

#### (6) Assumptions and Limitations of Regression Models

Regression models assume linearity in the response of the outcome variable to changes in independent variables. Linearity implies that the magnitude and direction of the response do not depend on the current level of the independent variable, and they also do not depend on other independent variables. The Board considers the linearity assumption to be reasonable for all
<!-- page 29 -->

cases in which it uses regression models to project pre-provision net revenue components and considers this choice consistent with the Policy Statement principle of simplicity. In this context, simplicity is a guiding principle since the use of non-linear methods would automatically imply a more complex and less concise statistical specification of the regression.

Further, the Board uses methods to address non-linearity within the regression framework, like interactions or the use of quadratic forms for independent variables, when it is necessary. For example, in the regression for interest expense on trading liabilities and other borrowed money, one of the independent variables (the U.S. Market Volatility Index) is used in a quadratic form in order to better address the non-linear response of the outcome variable.

Another assumption of the regression models is that all firms react equally to changes in the independent variables included in each regression. Again, the Board considers this assumption reasonable for all cases in which it is applied and judges this choice consistent with the Policy Statement principle of simplicity. In this context, simplicity is a guiding principle since the use of firm-specific coefficients would automatically imply a more complex and less concise statistical specification of the regression.

As previously described, for some components of pre-provision net revenue, the Board uses and estimates different regressions by groups of banks in order to address heterogeneity across banks. In these cases, firms in different groups can react differently to changes in independent variables, but it is still the case that, for a given group, all firms in that group react equally to changes in independent variables. There are other methods available within the regression framework to allow for heterogeneous responses to changes in independent variables that can vary by firm based on firm characteristics. The Board does not currently apply any such
<!-- page 30 -->

method to project pre-provision net revenue components, as their use implies a trade-off against the Policy Statement principle of consistency and comparability across firms.

One limitation of the regression models for pre-provision net revenue, as they are currently specified, is that the response of the outcome variables to changes in independent variables is symmetrical (in terms of magnitude, not direction) to both upward and downward movements in these independent variables. Thus, for instance, in a model which includes interest rates as independent variables, the dependent variable projections will react symmetrically to either a rise or a fall in interest rates (the projections will react at the same magnitude albeit in opposite directions). This is understood as a limitation because empirically there could exist some circumstances where the expected magnitude of the response of an outcome variable can be different for increases versus decreases in macroeconomic variables.

There are techniques available within the regression framework to apply asymmetrical responses of dependent variables to changes in independent variables in forecasting. The Board typically explores these techniques during the model selection process, but if they do not demonstrate superior and consistent out-of-sample performance, they are not the preferred approach. In future cycles of model redevelopment, the Board could adopt these alternatives if they are considered the preferred specification following the model selection process.

A limitation of the statistical approach is that the Board chooses models based on certain historical relationships and data availability at the time the model development and selection process took place. To the extent these relationships can change over time, the models will slowly incorporate these changes when they are re-estimated. However, to the extent the relationships deviate from the Board’s initial variable choices, the model will not capture these changes unless the model selection process is repeated. The Board recognizes that there is an
<!-- page 31 -->

inherent trade-off between basing model specifications on statistically significant historical relationships and recent behavior. Historically, the Board has engaged in new rounds of model selection and redevelopment on average at every three to four years, depending on the component. However, new model selection and development process can be triggered by the Board whenever it is necessary due to the evolution or changes in business models of firms or macroeconomic conditions.

The pre-provision net revenue models incorporate historical net interest income or expense trends to forecast post-stress revenues (or expenses) through the autoregressive terms or rolling-window fixed effects included in each regression. These models do not include separate adjustments to incorporate accretion schedules for fair-value marks, as this accretion is captured in income forecasts through historical net interest income trends.

Finally, income or expense related to interest rate hedging instruments is not directly modeled, although model coefficients for the regressions reflect the historical impact of hedging behavior on pre-provision net revenue components when such income or expense were present. Given its statistical nature, the current regression models of interest income and interest expense incorporate historical trends to forecast post-stress net revenues. The regression models thus reflect the historical impact of hedging behavior by firms and do not capture variation in hedging intensity between firms or over time. This is due to two data limitations: 1) historical effects of interest rate risk hedges are not separately reported, and 2) data to calculate the effects of interest rate risk hedges over the projection horizon are not currently available.

As discussed later in this document, the Board is proposing new models for pre-provision net revenue. The proposed models for net interest income would require further data collection in order to reflect the impact of hedges on projected post-stress net interest revenues. In the
<!-- page 32 -->

instance where the Board does not adopt the proposed models in 2026, the Board may explore the collection of additional data to identify the impact of interest rate risk hedging over the projection horizon in the current model.

<!-- Source PDF page 32 -->

<a id="sec-14"></a>

### b. Structural Models

Structural models directly calculate a revenue or expense projection based on economic relationships, the underlying contractual terms of the modeled component, and the asset or liability composition of each firm at the date of lift-off. Structural models are not statistical in nature but instead utilize a well-defined relationship between contracted financial instruments or balances at lift-off date, the expected income or expense flow, and the path of the interest rate in the scenario in order to calculate projections. The Board generally uses contractual obligations, applicable accounting rules, and scenario interest rate paths to generate projections for structural models.

The Board uses structural models in two distinct situations. First, the Board uses structural models to address firm heterogeneity when detailed, granular microdata is available and there is a strong conceptual relationship between one of the macroeconomic variables and the outcome variable (i.e., a relationship with interest rates) that is specific to the component. For instance, interest expense on subordinated debt is typically heterogeneous across firms and over time in terms of its composition and underlying parameters. In this case, the Board uses a structural model that projects expense from granular data for every financial instrument across firms since each instrument is typically indexed in terms of standard market interest rates.

Second, the Board uses structural models when the interest or expense component is homogeneous in composition (both within and across firms) and the expected flow of the income
<!-- page 33 -->

or expense component exhibits a static, pre-determined relationship with a macroeconomic variable, usually an interest rate. For example, the Board uses a structural model to project interest income and expense for federal funds sold and securities purchased under resale agreements or agreements to repurchase because these components respond directly and rapidly to short-term interest rate movements and are fairly homogeneous across firms.

<!-- Source PDF page 33 -->

<a id="sec-15"></a>

#### (1) Assumptions and Limitations of Structural Models

The Board uses structural models to address the complications that heterogeneity across firms introduces for regression models, but these models also present limitations.

Structural models assume strict relationships based on economic theory or the standing financial contracts held by firms. Further, for the models that use granular financial instruments data, the Board still needs to make some assumptions for the calculation of projections (e.g., regarding the re-origination of maturing instruments).

<!-- Source PDF page 33 -->

<a id="sec-16"></a>

### c. Nonparametric Models

The Board has determined that using a nonparametric model is appropriate to project revenues and expenses when the Board is unable to discern a clear and stable relationship between the component and macroeconomic scenario variables. In the clearest cases, a regression model may not be appropriate because of a lack of macroeconomic sensitivity and a high amount of heterogeneity in the component portfolios, because there may not be a well-founded case for a structural model, and because the elevated heterogeneity on the behavior of the component across banks and over time may make a discount path model infeasible.
<!-- page 34 -->

<!-- Source PDF page 34 -->

<a id="sec-17"></a>

#### (1) Method Description

The Board uses nonparametric models to create flat projections over the projection horizon. The Board uses the firm-level median observed over the most recent eight quarters to project certain pre-provision net revenue components. The median is calculated from the ratio of the respective income or expense flow divided by a relevant balance variable (most frequently, total assets for the component). As a final step, the calculated firm-level median is multiplied by the respective firm balances to calculate projections in dollars. The eight-quarter timeframe reflects recent activity while also mitigating the impact of input data volatility in any given quarter. One example of a component projected using a nonparametric model is all other noninterest expense.

<!-- Source PDF page 34 -->

<a id="sec-18"></a>

#### (2) Assumptions and Limitations of Nonparametric Models

The central assumptions underlying the use of nonparametric models that are based on the recent firm-level median are:

- that the last two years of observed values for the revenue or expense component are representative of future performance, and thus useful for forecasting; and
- that the revenue or expense component is not expected to vary based on macroeconomic conditions or economic distress.

The relevant consequences and limitations of these assumptions are that projections under nonparametric models are fixed for each firm, they depend on the starting firm-level conditions (the last eight quarters of performance), and they do not vary according to the scenario being forecasted.
<!-- page 35 -->

<!-- Source PDF page 35 -->

<a id="sec-19"></a>

### d. Data Sources and Treatment

<!-- Source PDF page 35 -->

<a id="sec-20"></a>

#### (1) Pro Forma Adjustment Process

The Board uses data from the FR Y-9C and FR Y-14Q reports, some of which provide data from as early as 1991, to estimate model coefficients (in the case of regressions), to calculate values of balances and flows at lift-off, to calculate discount paths, and as an input to structural models. Over time, many firms subject to the supervisory stress test have changed their business models via mergers, acquisitions, or divestitures. Therefore, to create a time series that reflects each firm’s business and current risk profile at the starting point of each supervisory stress test as well as to provide a consistent history of data for model estimation, the Board adjusts the historical regulatory data to account for these changes. Specifically, the Board combines the financial data for each institution that has been acquired by a given firm over all the historical years available. This process is referred to as the pro forma adjustment.

The pro forma adjustment is a straightforward way to represent the current business mix of the set of stress tested banks as if it had existed consistently over time. For example, suppose that a bank (subject to stress testing) focused only on lending acquires a trading institution. The new firm will have a combined business mix of lending and trading, and this combined revenue mix is important to be used for pre-provision net revenue projection. However, the past time series from FR Y-9C for the lead bank will not have any trading revenue registered. This will harm the estimation of bank-specific parameters in the regression. The pro forma process combines the past revenue and expenses of both firms (lead and acquired institution) as if they have existed in the past as a consolidated unit. This process allows for estimation of bank-specific parameters that take into account the current revenue and expense mix.
<!-- page 36 -->

The pro forma adjustment aligns with two of the principles from the Board’s Policy Statement. First, the adjustment promotes consistency and comparability by mitigating the potential sudden impact of a business plan change. Second, it leads to more robust and stable model projections, as more data points, and data points containing more useful information over a longer time horizon, can be used to calculate projections.

The pro forma adjustment process involves several steps. First, the Board identifies entities that have merged using structural data from the National Information Center on mergers, as well as relationship data that identify the top U.S. holding company parent institution (top holder). For every entity with a Research, Statistics, Supervision, and Discount Identifier (RSSD ID), the Board constructs a mapping between RSSD IDs and top holders. To do this, the Board traces merger chains to the top holder using the relationships data from the National Information Center. For these adjustments, the Board also complements available FR Y-9C data with data from the Thrift Financial Report Form 1313 and the Consolidated Reports of Condition and Income (FFIEC 031 and 041) *.*

While the use of pro forma data reduces merger-related discontinuities, it may not eliminate them entirely. First, not all mergers, acquisitions, or portfolio changes can be included in the merger-adjusted data. For example, the pro forma adjustment process does not capture asset acquisitions and divestitures, such as of a credit card portfolio, unless entire companies are acquired. Second, some mergers and acquisitions involve unregulated entities without viable historical reporting that can be included in the data. Where possible, the Board identifies these mergers using the National Information Center data in conjunction with other databases. When the event entails substantial and sudden variation in firm balances’ composition or performance, and in the case of components using regression models for projections, the Board incorporates
<!-- page 37 -->

possible firm-breaks into the dataset and regression equations. Firm-breaks are a type of fixed effects added to regression input datasets and to equations that aim to capture major firm-specific events. They are discussed previously in subsection “Addressing Firm Heterogeneity: Firm Characteristics, Fixed Effects, and Grouping.”

<!-- Source PDF page 37 -->

<a id="sec-21"></a>

#### (2) Data Sources

The Board uses data from the FR Y-9C as input to most regression models. Each component flow of income or expense, as well as the asset or liability balance, is calculated from one or more corresponding variable from FR Y-9C. The variables on FR Y-9C are identified by mnemonics, or code names. Table A2 below presents the mapping for each component flow to their corresponding variable mnemonic calculation.

**Table A2** –Component Flows and Corresponding Variable Mnemonic Calculation

| Component flow | Calculation from mnemonic | Source |
|---|---|---|
| interest income on loans | BHCK4435 + BHCK4436, BHCKF821 + BHCK4059 + BHCK4065 | FR Y-9C |
| interest income on U.S. Treasuries | BHCKB488 | FR Y-9C |
| interest income on mortgage-backed securities | BHCKB489 | FR Y-9C |
| interest income from other securities | BHCK4060 | FR Y-9C |
| interest income from trading assets | BHCK4069 | FR Y-9C |
| all other interest income | BHCK4518 | FR Y-9C |
| interest income from federal funds sold and securities purchased under agreements to resell | BHCK4020 | FR Y-9C |
| interest expense on domestic time deposits | BHCKHK03 + BHCKHK04 | FR Y-9C |
| interest expense on other domestic deposits | BHCK6761 | FR Y-9C |
| interest expense on foreign deposits | BHCK4172 | FR Y-9C |
| interest expense on trading liabilities, other borrowed money and all other interest expense | BHCK4185 + BHCK4398 | FR Y-9C |
| interest expense on federal funds purchased and securities sold under agreements to repurchase | BHCK4180 | FR Y-9C |
| trading revenue | BHCKA220 | FR Y-9C |
| noninterest income from service charges on deposits | BHCK4483 | FR Y-9C |
| noninterest income from net servicing fees | BHCKB492 | FR Y-9C |
| noninterest income from investment banking fees | BHCKC886 + BHCKC888 + BHCKB491 | FR Y-9C |
| noninterest income from fiduciary income and insurance banking fees | BHCK4070 + BHCKC887 + BHCKC386 + BHCKC387 | FR Y-9C |
| noninterest expense from compensation | BHCK4135 | FR Y-9C |
| noninterest expense on fixed assets | BHCK4217 | FR Y-9C |

<!-- page 38 -->

Table A3 presents the mapping for each component’s corresponding balances to their variable mnemonic calculation.

**Table A3 –Component Balances and Corresponding Variable Mnemonic Calculation**

| Balances | Calculation from mnemonic | Source |
|---|---|---|
| total loans | BHCK2122 | FR Y-9C |
| U.S. Treasury Securities | BHCK0211 + BHCKHT50 + BHCK1287 + BHCKHT53 | FR Y-9C |
| mortgage-backed securities | BHCK(G300 + G304 + G308 + G312 + G316 + G320 + K142 + K146 + K150 + K154 + G303 + G307 + G311 + G315 + G319 + G323 + K145 + K149 + K153 + K157) | FR Y-9C |
| other securities | BHCK(1737 + 1742 + C026 + HT58 + 1741 + 1746 + A511 + C027 + HT61 + 8496 + 8499) + BHCKJA22 | FR Y-9C |
| trading assets | BHCK3545 | FR Y-9C |
| assets underlying federal funds sold and securities purchased under the agreement to resell | BHDMB987 + BHCKB989 | FR Y-9C |
| total interest earning assets | BHCK2122 + BHDMB987 + BHCKB989 + BHCK1754 + BHCK1773 + BHCK0395 + BHCK0397 + BHCK3545 + BHCKJA22 | FR Y-9C |
| domestic time deposits | BHCBJ474 + BHODJ474 + BHCBHK29 + BHODHK29 | FR Y-9C |
| other domestic deposits | BHCB3187 + BHOD3187 + BHCB2389 + BHOD2389 | FR Y-9C |
| total foreign deposits | BHFN6631 + BHFN6636 | FR Y-9C |
| trading liabilities and other borrowed money | BHCK3548 + BHCK3190 | FR Y-9C |
| liabilities underlying federal funds purchased and securities sold under the agreement to repurchase | BHDMB993 + BHCKB995 | FR Y-9C |
| total deposits | BHDM6631 + BHDM6636 + BHFN6631 + BHFN6636 | FR Y-9C |
| total servicing assets | BHCK3164 | FR Y-9C |
| total assets | BHCK2170 | FR Y-9C |

<!-- page 39 -->

<!-- Source PDF page 39 -->

<a id="sec-22"></a>

### e. Subordinated Debt Data Construction

The Board uses instrument-level data from the FR Y-14Q report to project subordinated debt expenses in the supervisory stress test. Although each firm is required to submit complete and accurate reports, the data sometimes lack information due to the number of details required for each instrument. For example, a maturity or closing date for a security (which is important in projecting subordinated debt expense) might be missing. In these cases, the Board uses vendor data to fill in missing information and verifies the details with the submitting firm.

<!-- Source PDF page 39 -->

<a id="sec-23"></a>

## iii. Questions

*Question A1: What are the advantages and disadvantages of the data adjustments the Board makes to construct the pro forma data when modeling pre-provision net revenue components? What alternatives should the Board consider, if any, to account for notable business*
<!-- page 40 -->

*changes or different reporting of data due to events such as accounting changes over time? What would be the advantages and disadvantages of these alternatives?*

*Question A2: Are there additional data adjustment or cleaning steps the Board should consider when modeling pre-provision net revenue components? If so, what are they? What would be the advantages and disadvantages of those steps?*
<!-- page 41 -->

<!-- Source PDF page 41 -->

<a id="sec-24"></a>

## iv. Pre-Provision Net Revenue Model Components

<!-- Source PDF page 41 -->

<a id="sec-25"></a>

### a. Regression Models for Interest Income

Net interest income is defined as interest income less interest expense. The Board models seven of the eight interest income components in the pre-provision net revenue model suite using the panel regression framework previously described. These components are:

- interest income on loans,
- interest income on interest-bearing balances,
- interest income on U.S. Treasuries,
- interest income on mortgage-backed securities,
- interest income on other securities,
- interest income from trading assets, and
- all other interest income. In accordance with criteria previously provided in Section A.ii.a.(1) Justification for the Use of Regression Models, the Board has determined that these seven components are well suited to the regression framework because they:
- are reported consistently across firms and over time in the FR Y-9C, with a long time series of data available for model estimation; and
- are responsive to macroeconomic factors (typically to interest rate levels), and these relationships are statistically strong and economically significant.

Furthermore, the regression models for interest income have generally demonstrated good out-of-sample performance during model selection tests, specifically for periods of economic distress, and high in-sample fit.

The Board also models one interest income component using the structural approach: interest income from federal funds sold and securities purchased under agreements to resell. The Board chose to model this component using a structural approach after determining that the regression framework was not appropriate. For this component, the Board verified the existence
<!-- page 42 -->

of homogeneity in asset composition and a clear economic relationship between expected revenues, the asset balances of each firm, and the expected path of the interest rate. This component is discussed further in a later section dedicated to structural models.

<!-- Source PDF page 42 -->

<a id="sec-26"></a>

### b. Interest Income on Loans

<!-- Source PDF page 42 -->

<a id="sec-27"></a>

#### (1) Description

Interest income on loans comprises interest and fee income on loans in domestic and foreign offices including loans secured by real estate plus income from lease financing receivables as reported in the Consolidated Financial Statements for Holding Companies FR Y-9C, Report of Income for Holding Companies, Schedule HI. The dependent variable in this model regression is the ratio of this income normalized by the balance of total loans[^16].

Interest income on loans is a major income stream for all firms in the panel and varies by loan type and business cycle. For example, as interest rates rise, firms charge higher interest rates on variable-rate loans (such as credit card loans) and fixed-rate originations (e.g., mortgage loans). When rates fall, firms earn less interest income on real estate loans, as borrowers seek to refinance to lower rates. Interest rate-related variables are thus key inputs into the interest income on loans model.

<!-- Source PDF page 42 -->

<a id="sec-28"></a>

#### (2) Model Specification

In the interest income on loans regression model, the projected component ratio is correlated with U.S. Treasury rates, characteristics of each firm’s loan portfolio, and the average level of the component ratio for each firm.
<!-- page 43 -->

The model is specified according to the following equation:

**Equation A3** – Interest Income on Loans Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 Treasury3m(t) + \beta_2 TermSpread10yLag(t) + \beta_3 ShareCCLoans(b,t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where*

- $Ratio(b,t) = \frac{\text{interest income on loans}_{b,t}}{\text{total loans}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;
- $TermSpread10yLag(t)$ is the one-quarter lag of the term spread (10-year Treasury yield minus the 3-month Treasury yield), representing future interest rate expectations and the term premium measured during the previous quarter;
- $ShareCCLoans(b,t)$ is the share of credit card loans to total loans for each firm in each quarter, to account for the higher return of the credit card loan portfolio when compared to other types of lending;
- $\alpha_b$ represents firm-level fixed effects, accounting for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<a id="sec-29"></a>

#### (3) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.), for the interest income on loans component model. In particular, the Board observed in the historical data series that the interest income on loans ratio responds positively to short-term rate increases and to increases in the term spread. This relationship reflects income from variable-rate loans and the issuance of new fixed-rate loans at prevailing rates, which increases when rates rise. The Board also observed that movements in interest rate expectations and in the term premium require a period of at least one quarter to fully pass through to average loan yield in the portfolio.
<!-- page 44 -->

Following the standard procedure for macroeconomic variable selection, the macroeconomic variables selected for this model were the 3-month Treasury yield and the one-quarter lag of the 10-year term spread. These variables demonstrated the best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and did not show signs of model instability when re-estimated at different starting points. The lag of the 10-year term spread demonstrated better predictive power compared to other variables measuring the term spread. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold. As previously stated in the Macroeconomic Variable Selection Section A.ii.a.(3)(c.), the defined threshold is 5% enhancement in out-of-sample forecasting performance in terms of root-mean squared error.

The model specification also includes a variable accounting for each firm’s share of credit card loans to total loans because the Board observed that interest income on loans is higher for institutions with a greater share of credit card loans. The Board also tested other, similar independent variables available from FR Y-9C data representing the relative shares of other types of loans. However, only the share of credit card loans materially increased the predictive power of the model.

The Board also observed that, as market interest rates move during an economic cycle, the average yield on loan portfolios follows. However, the adjustment is not immediate and depends on the duration (average time it takes to receive the cash flows) of the portfolio. The Board accounts for the relationship between previous performance of the dependent variable and future outcomes by including a Year AR term in the model specification.

The model specification also captures firm heterogeneity by including firm-level and rolling-window fixed effects. Firm-level fixed effects account for differences between firm
<!-- page 45 -->

portfolios, while rolling-window fixed effects account for recent changes in firms’ business models.

<!-- Source PDF page 45 -->

<a id="sec-30"></a>

#### (4) Assumptions and Limitations

Among limitations previously discussed, regression models assume linearity in the response of the dependent variable to changes in macroeconomic variables. As a consequence, for the interest income on loans component model, coefficients on macroeconomic variables thus reflect average historical repricing behavior as interest rates vary. Another assumption of the model is that all firms react equally and symmetrically to changes in the macroeconomic variables included in the regression. Increases in the U.S. Treasury rate or in the term spread will result in higher interest income for all firms at the same rate. Note that the inclusion of firm level and rolling-window fixed effects is not related to this issue. Fixed effects are related to the average level of the dependent variable over time, not to the sensitivity of the dependent variable to changes in macroeconomic variables.

Alternative modeling options within the regression framework, such as non-linear models or interactions, could offer more flexibility to address asymmetrical responses and provide more conservative projection outcomes under stress. However, models with asymmetrical macroeconomic sensitivity, which depend on the direction of the interest rate change, are not always preferable. They could provide more conservative projections for interest income under scenarios of falling interest rates when compared to simple linear models but may also introduce higher variance on projections across stress testing cycles as the regression model is re-estimated given the high correlation between independent variables.
<!-- page 46 -->

Additional alternative modeling options within the regression framework could allow for, given a change in interest rates, different changes in income across firms (allowing for heterogeneity) based on firm portfolio characteristics or composition (e.g., loan types, average durations, and average origination dates). This option would require additional data beyond what is currently used in the regression model. This approach would require long historical data from every firm to assure a low variance of regression estimates. This could represent a limitation for firms entering the sample at later dates since they would not be able to provide long historical time series.

The Board understands that the current regression model for interest income on loans to be appropriate given the behavior of the underlying variables and consistent with the Policy Statement principle of simplicity and considers this model to be as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

Structural model alternatives use instrument-level microdata from banks’ loan holdings at the stress test starting point in order to project expected earnings. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on the structural approach.

<!-- Source PDF page 46 -->

<a id="sec-31"></a>

#### (5) Questions

*Question A3: The Board seeks comment on the structural model alternative that uses instrument-level microdata, as compared to the Board's current approach of using a panel regression model.*
<!-- page 47 -->

*Question A4: Is there any other alternative model that the Board should consider to project interest income on loans? What would be the advantages and disadvantages of using that alternative to project interest income on loans?*

*Question A5: Are there additional factors that the Board should consider in modeling interest income on loans? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A6: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest income on loans?*

*Question A7: Are there additional data sources the Board should consider incorporating in its modeling of interest income on loans? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

*Question A8: What are the best options to identify and account for the impact of interest rate risk hedging on loan income under stress test scenarios? What kind of data collection would this require? Would it be useful to collect information that decomposes contractual payments for each securities from details related to hedges in order to more precisely estimate the exposure of banks to scenarios?*

*Question A9: Regarding improvements to the current regression approach for modeling interest income on loans, should the model explicitly account for asymmetry in prepayment behavior? Are there other nonlinearity concerns that should be addressed in the model? What are possible technical solutions that could be suggested to approach nonlinearity? What are the advantages and disadvantages of these solutions?*
<!-- page 48 -->

<!-- Source PDF page 48 -->

<a id="sec-32"></a>

### c. Interest Income on Interest-Bearing Balances

<!-- Source PDF page 48 -->

<a id="sec-33"></a>

#### (1) Description

Interest income from interest-bearing balances consists of interest-bearing deposits, including deposits held at other institutions such as the Federal Home Loan Banks and at the Federal Reserve.[^17] These balances have short durations, typically less than a single quarter and the yield earned is usually directly linked to short-term interest rates.

<!-- Source PDF page 48 -->

<a id="sec-34"></a>

#### (2) Model Specification

In the interest income from interest-bearing balances regression model, the projected component ratio is correlated with U.S. Treasury rates, the term spread, and the average level of the component ratio for each firm.

The model is specified according to the following Equation A4:

**Equation A4 – Interest Income from Interest-Bearing Balances Regression Model**

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 Treasury3m(t) + \beta_2 TermSpread10yLag(t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where*

- $Ratio(b,t) = \frac{\text{interest income on interest bearing balances}_{b,t}}{\text{interest bearing balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed in the previous four quarters;
- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;
- $TermSpread10yLag(t)$ is the one-quarter lag of the term spread (10-year Treasury yield minus the 3-month Treasury yield), representing future interest rate expectations and the term premium measured during the previous quarter;

<!-- page 49 -->

- $\alpha_b$ represents firm-level fixed effects, accounting for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 49 -->

<a id="sec-35"></a>

#### (3) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.), for the interest income from interest-bearing balances component model. In particular, the Board observed in the historical data series that the interest income on interest bearing balances ratio responds positively to short-term rate increases and to increases in the term spread. This relationship reflects income from interest-paying balances held as deposits by other financial institutions, which increases when rates rise. The Board also observed that movements in interest rate expectations and in the term premium require a period of at least one quarter to fully pass through to average yield in the portfolio.

Following the standard procedure for macroeconomic variable selection, the macroeconomic variables selected for this model were the 3-month Treasury yield and the one-quarter lag of the 10-year term spread. These variables demonstrated the best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and did not show signs of model instability when re-estimated at different starting points. The lag of the 10-year term spread demonstrated better predictive power compared to other variables measuring the term spread. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold. As previously stated on the Macroeconomic Variable Selection section A.ii.a.(3)(c.), the defined threshold is 5% enhancement in out-of-sample forecasting performance in terms of root-mean squared error.
<!-- page 50 -->

The Board also observed that, as market interest rates move during an economic cycle, the average yield on interest-bearing balances also follows. However, the adjustment is not immediate and depends on the duration (average time it takes to receive the cash flows) of the portfolio. The Board accounts for this persistence in the projections by including a Year AR term in the model specification.

The model specification also captures firm heterogeneity by including firm-level and rolling-window fixed effects. Firm-level fixed effects account for differences between firm positions held as assets earning interest income, while rolling-window fixed effects account for recent changes in firms’ business models.

<!-- Source PDF page 50 -->

<a id="sec-36"></a>

#### (4) Assumptions and Limitations

As discussed previously, regression models assume linearity in the response of the dependent variable to changes in macroeconomic variables. As a consequence, for the interest income on interest-bearing balances component model, coefficients on macroeconomic variables thus reflect average historical repricing behavior as interest rates vary. Another assumption of the model is that all firms react equally and symmetrically to changes in the macroeconomic variables included in the regression. Increases in the U.S. Treasury rate or in the term spread will result in higher interest income for all firms at the same rate. Note that the inclusion of firm level and rolling-window fixed effects is not related to this issue. Fixed effects are related to the average level of the dependent variable over time, not to the sensitivity of the dependent variable to changes in macroeconomic variables.

Alternative modeling options within the regression framework, such as non-linear models or interactions, could offer more flexibility to address asymmetrical responses and provide more
<!-- page 51 -->

conservative projection outcomes under stress. However, models with asymmetrical macroeconomic sensitivity, which depend on the direction of the interest rate change, are not always preferable. They could provide more conservative projections for interest income under scenarios of falling interest rates when compared to simple linear models but may also introduce higher variance on projections across stress testing cycles as the regression model is re-estimated given the high correlation between independent variables.

The Board understands that the current regression model for interest income on interest-bearing balances to be appropriate given the behavior of the underlying variables and consistent with the Policy Statement principle of simplicity and considers this model to be as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

Structural model alternatives could also be used to model interest income from interest-bearing balances. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on the structural approach.

<!-- Source PDF page 51 -->

<a id="sec-37"></a>

#### (5) Questions

*Question A10: The Board seeks comment on the structural model alternative that uses instrument-level microdata, as compared to the Board's current approach of using a panel regression model.*

*Question A11: Is there any other alternative model that the Board should consider to project interest income from interest-bearing balances? What would be the advantages and*
<!-- page 52 -->

*disadvantages of using that alternative to project interest income from interest-bearing balances?*

*Question A12: Are there additional factors that the Board should consider in modeling interest income from interest-bearing balances? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A13: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest income from interest-bearing balances?*

*Question A14: Are there additional data sources the Board should consider incorporating in its modeling of interest income from interest-bearing balances? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 52 -->

<a id="sec-38"></a>

### d. Interest Income on U.S. Treasuries

<!-- Source PDF page 52 -->

<a id="sec-39"></a>

#### (1) Description

Interest income on U.S. Treasuries comprises interest and dividend income on U.S. Treasury securities and U.S. government agency obligations (excluding mortgage-backed securities). The dependent variable used in this model regression is the ratio of this income normalized by the balances of U.S. Treasury Securities.[^18] Treasury securities include bonds, Treasury bills, Treasury notes, and Treasury inflation-protected securities (TIPS). U.S.
<!-- page 53 -->

government agency debt obligations are bonds or debt securities issued by either U.S. government agencies or government-sponsored enterprises (GSEs).

<!-- Source PDF page 53 -->

<a id="sec-40"></a>

#### (2) Model Specification

In the interest income on U.S. Treasuries regression model, the projected ratio is correlated with U.S. Treasury rates and the average level of the ratio for each firm.

The model is specified according to the following equation:

**Equation A5** – Interest Income on U.S. Treasuries Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 Treasury3m(t) + \beta_2 TermSpread5y(t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where*

- $Ratio(b,t) = \frac{\text{interest income on U.S. Treasuries}_{b,t}}{\text{U.S. Treasury securities balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;
- $TermSpread5y(t)$ is the 5-year term spread (5-year Treasury yield minus the 3-month Treasury yield), representing future interest rate expectations and the term premium;
- $\alpha_b$ represents firm-level fixed effects, which accounts for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 53 -->

<a id="sec-41"></a>

#### (3) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.): Variable Selection for this model. In particular, the Board observed in the historical data series that the interest income on U.S. Treasuries ratio responds positively to
<!-- page 54 -->

short-term rate increases and to increases in the 5-year term spread. These relationships reflect the adjustment of earnings in the Treasury portfolio to changes in interest rate yields.

The macroeconomic variables selected to be part of this model are the 3-month Treasury yield and the 5-year term spread. These variables demonstrated the best out-of-sample forecasting performance of the variables considered, provided macroeconomic sensitivity in stressed scenarios, and did not show signs of model instability when re-estimated at different starting points. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold.

Firms may have variable preferences for holding different portfolios of U.S. Treasuries (for example, different portfolio composition in terms of maturities and origination dates), which implies, in turn, that firms will earn different average yields over time. The regression model accounts for this fact by including the autoregressive term and firm-level fixed effects.

The model does not identify material cross-sectional differences in firms’ sensitivity to rates. Model projections for this component perform well out of sample and the model selection procedure for the identification of groups did not produce improvements in forecast performance by adopting distinct groups in modeling.

<!-- Source PDF page 54 -->

<a id="sec-42"></a>

#### (4) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity in the response of the dependent variable to changes in macroeconomic variables. For the interest income on U.S. Treasuries component model, coefficients on macroeconomic variables thus reflect the average historical portfolio yield adjustment as interest rates vary.
<!-- page 55 -->

Given the relative homogeneity and stability of this portfolio, as for example it is not subject to prepayment and credit risk, the Board understands that the linear regression model choice is appropriate and consistent with the Policy Statement principle of simplicity and considers it as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

Structural model alternatives use instrument-level microdata from banks’ holdings of U.S. Treasuries at the stress test starting point in order to project earnings. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on the structural approach.

<!-- Source PDF page 55 -->

<a id="sec-43"></a>

#### (5) Questions

*Question A15: The Board seeks comment on the structural model alternative that uses instrument-level microdata, as compared to the Board's current approach of using a panel regression model.*

*Question A16: Is there any other alternative model that the Board should consider to project interest income on U.S. Treasuries? What would be the advantages and disadvantages of using that alternative to project interest income on U.S. Treasuries?*

*Question A17: Are there additional factors that the Board should consider in modeling interest income on U.S. Treasuries? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*
<!-- page 56 -->

*Question A18: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest income on U.S. Treasuries?*

*Question A19: Are there additional data sources the Board should consider incorporating in its modeling of interest income on U.S. Treasuries? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 56 -->

<a id="sec-44"></a>

### e. Interest Income on Mortgage-Backed Securities

Interest income on mortgage-backed securities includes interest and dividend income on mortgage-backed securities held at fair value. The dependent variable used in this model regression is the ratio of this income normalized by the balance of mortgage-backed securities.[^19]

Mortgage-backed securities are created by pooling mortgage loans into a single instrument that earns income from the repayment of those underlying loans. These loans can be commercial or residential and are issued, insured, or held by U.S. government institutions (agencies) and other lenders (non-agencies) including non-banks. These loans present a range of risks and exposures depending on the type of loan and the issuer of the underlying securities. Firms assemble their portfolio of mortgage-backed securities according to their risk appetites. For example, commercial mortgage-backed securities are composed of pooled commercial real estate loans and are therefore exposed to the commercial real estate market. U.S. government
<!-- page 57 -->

agency securities[^20] and government-sponsored enterprise-backed securities[^21] are generally considered safer because the payment of the principal and interest on their underlying loans is guaranteed by the U.S. government or GSEs.

<!-- Source PDF page 57 -->

<a id="sec-45"></a>

#### (1) Model Specification

In the interest income on mortgage-backed securities regression model, the projected ratio is correlated with U. S. Treasury rates and the average level of the ratio for each firm.

The model is specified according to the following equation:

**Equation A6** – Interest Income on Mortgage-Backed Securities Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 Treasury3mLag(t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where*

- $Ratio(b,t) = \frac{\text{interest income on mortgage-backed securities}_{b,t}}{\text{mortgage-backed securities balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $Treasury3mLag(t)$ is the one-quarter lag of the 3-month Treasury yield, representing the risk-free short-term rate measured at the previous quarter;
- $\alpha_b$ represents firm-level fixed effects, accounting for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 57 -->

<a id="sec-46"></a>

#### (2) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.), for this model. In particular, the Board observed in the historical data
<!-- page 58 -->

series that the interest income on mortgage-backed securities ratio responds positively, and with a lag, to short-term rate increases. This relationship reflects the adjustment of the average yield to changing market interest rates. Since the average time-to-maturity of mortgage-backed securities is relatively long, and a large share of the portfolio is fixed rate, changes in current market conditions are not immediately passed through to yields.

Following the standard procedure for macroeconomic variable selection, the macroeconomic variable selected to be part of this model is the 3-month Treasury yield with a one-quarter lag. This variable demonstrated the best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and did not show signs of model instability when re-estimated at different starting points. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold.

The Board has observed that interest income on mortgage-backed securities achieved in previous periods is correlated with future outcomes. The regression model accounts for this relationship by including a Year AR term.

Firms hold different portfolios of mortgage-backed securities, which can vary in risk level, origination date, and duration. This implies, in turn, different average yields across firms. The regression model accounts for this by including firm-specific fixed effects. Recent changes in firms’ portfolio holdings are captured by the rolling-window fixed effects.

<!-- Source PDF page 58 -->

<a id="sec-47"></a>

#### (3) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity in the response of the dependent variable to changes in macroeconomic variables. For
<!-- page 59 -->

the interest income on mortgage-backed securities model, coefficients on macroeconomic variables thus reflect average historical portfolio yield adjustments as interest rates vary. The model also assumes that all firms react equally to changes in the macroeconomic variables in the regression. Increases in the Treasury rate will result in higher interest income for all firms at the same rate. Note that the inclusion of firm-level and rolling-window fixed effects is not related to this issue. Fixed effects are related to the average level of the dependent variable over time, not to the sensitivity of the dependent variable to changes in macroeconomic variables.

The Board understands that the current regression model for interest income on mortgage-backed securities is appropriate and consistent with the Policy Statement principle of simplicity and considers it as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

Structural model alternatives use instrument-level microdata from banks’ holdings of mortgage-backed securities at the stress test starting point in order to project earnings. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on the structural approach.

<!-- Source PDF page 59 -->

<a id="sec-48"></a>

#### (4) Questions

*Question A20: The Board seeks comment on the structural model alternative that uses instrument-level microdata, as compared to the Board's current approach of using a panel regression model.*
<!-- page 60 -->

*Question A21: Is there any other alternative model that the Board should consider to project interest income on mortgage-backed securities? What would be the advantages and disadvantages of using that alternative to project interest income on mortgage-backed securities?*

*Question A22: Are there additional factors that the Board should consider in modeling interest income on mortgage-backed securities? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A23: Are there additional data reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest income on mortgage-backed securities?*

*Question A24: Are there additional data sources the Board should consider incorporating in its modeling of interest income on mortgage-backed securities? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 60 -->

<a id="sec-49"></a>

### f. Interest Income on Other Securities

Interest income on other securities includes income from all securities reportable as securities issued by states and political subdivisions in the U.S., asset-backed securities, other debt securities, and investments in mutual funds and other equity securities with readily determinable fair values (BHCK4060). The dependent variable used in this model regression is the ratio of this income normalized by the balances of other securities.[^22]
<!-- page 61 -->

Other securities are pooled instruments backed by a variety of types of loans (commonly auto loans, student loans, and others), debt (like bonds), or other types of assets. The underlying securities may have diverse credit risk profiles and a range of yields and maturities. The Board has observed that historically, and as demonstrated during the 2008 financial crisis, income from other securities is responsive to financial conditions.

<!-- Source PDF page 61 -->

<a id="sec-50"></a>

#### (1) Model Specification

In the interest income on other securities regression model, the projected ratio is correlated with U.S. Treasury rates, corporate credit spreads, and the average level of the ratio for each bank.

The model is specified according to the following equation:

**Equation A7** – Interest Income on Other Securities Regression Model

$$Ratio(b,t) = \beta_1 Treasury3m(t) + \beta_2 TermSpread10y(t) + \beta_3 BBBSpread10y(t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where*

- $Ratio(b,t) = \frac{\text{interest income on other securities}_{b,t}}{\text{other securities balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;
- $TermSpread10y(t)$ is the 10-year term spread (10-year Treasury yield minus the 3-month Treasury yield), representing future interest rate expectations and the term premium;
- $BBBSpread10y(t)$ is the spread of the BBB Bond Index Yield to the 10-year Treasury yield (BBB Bond Index Yield minus the 10-year Treasury yield), representing financial conditions;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- page 62 -->

<!-- Source PDF page 62 -->

<a id="sec-51"></a>

#### (2) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.). In particular, the Board observed in the historical data series that the interest income on other securities ratio responds positively to short-term rate increases and to increases in the term spread. This relationship reflects the adjustment of the average yield to changing market interest rates. The Board has also observed in the historical data series that the ratio of interest income on other securities also responds positively to increases in the BBB Bond Yield Index spread. This relationship reflects the upward adjustment of average earnings on other securities when financial conditions tighten. Higher sensitivity to credit risk in this portfolio, caused by riskier underlying assets compared with other portfolios, explains the series’ responsiveness to the BBB spread.

Following the standard procedure for macroeconomic variable selection, the Board selected three macroeconomic variables for this model: the 3-month Treasury yield, the 10-year term spread, and the spread of the BBB Bond Index Yield to the 10-year Treasury yield. This group of variables demonstrated the best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and did not show signs of model instability when re-estimated at different starting points. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold.

Firms have differing preferences for holding portfolios of other securities, which can vary in risk, origination date, and duration. This implies, in turn, different average yields across firms. The regression model accounts for this by including firm-specific fixed effects. Recent changes in firms’ portfolio holdings are captured by rolling-window fixed effects.
<!-- page 63 -->

During the model selection procedure, the Year AR term did not show statistical significance in the regressions. Thus, the Year AR term is not included in this regression specification. As a consequence, the projections for this component typically respond rapidly to changes in market rates and financial conditions.

<!-- Source PDF page 63 -->

<a id="sec-52"></a>

#### (3) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity in the response of the dependent variable to changes in macroeconomic variables. For the other securities model, coefficients on macroeconomic variables thus reflect average historical portfolio yield adjustment as interest rates and corporate credit spreads change. The model also assumes that all firms react equally to changes in the macroeconomic variables included in the regression. Increases in the Treasury rate, in the term spread or in the BBB credit spread will result in higher interest income for all firms, at the same rate. Note that the inclusion of firm-level and rolling-window fixed effects is not related to this issue. Fixed effects are related to the average level of the dependent variable over time, not to the sensitivity of the dependent variable to changes in macroeconomic variables.

The Board understands that the linear regression model for interest income on other securities is appropriate and consistent with the Policy Statement principle of simplicity as it is considered as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

Structural model alternatives use instrument-level microdata from banks’ holdings of other securities at the stress test starting point in order to project earnings. As discussed in
<!-- page 64 -->

Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on the structural approach.

<!-- Source PDF page 64 -->

<a id="sec-53"></a>

#### (4) Questions

*Question A25: The Board seeks comment on the structural model alternative that uses instrument-level microdata, as compared to the Board's current approach of using a panel regression model.*

*Question A26: Is there any other alternative model that the Board should consider to project interest income on other securities? What would be the advantages and disadvantages of using that alternative to project interest income on other securities?*

*Question A27: Are there additional factors that the Board should consider in modeling interest income on other securities? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A28: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest income on other securities?*

*Question A29: Are there additional data sources the Board should consider incorporating in its modeling of interest income on other securities? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

*Question A30: Should the panel regression model explicitly account for portfolio composition (maturities, origination date, types of securities) to project interest income on other securities? What would be the advantages or disadvantages of any such approach?*
<!-- page 65 -->

*Question A31: Are there any nonlinearity concerns that should be addressed in the model to project interest income on other securities? How should they be addressed, and what would be the advantages or disadvantages of these approaches?*

<!-- Source PDF page 65 -->

<a id="sec-54"></a>

### g. Interest Income from Trading Assets

Interest income from trading assets[^23] includes all interest income earned on trading assets and the accretion of discounts on assets held in trading accounts that have been issued on a discount basis (e.g., U.S. Treasury bills and commercial paper) but excludes trading gains and losses and fees from assets held in trading accounts. The dependent variable in this model regression is the ratio of this income normalized by the balance of trading assets.[^24]

<!-- Source PDF page 65 -->

<a id="sec-55"></a>

#### (1) Model Specification

In the interest income on trading assets regression model the projected ratio is correlated with U.S. Treasury rates, corporate credit spreads, and the average level of the ratio for each bank.

The model is specified according to the following equation:

**Equation A8** – Interest Income on Trading Assets Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 Treasury3m(t) + \beta_2 BBBSpread10y(t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where:*

<!-- page 66 -->

- $Ratio(b,t) = \frac{\text{interest income on trading assets}_{b,t}}{\text{trading assets balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;
- $BBBSpread10y(t)$ is the spread of the BBB Bond Index Yield to the 10-year Treasury yield (BBB Bond Index Yield minus the 10-year Treasury yield), representing financial conditions;
- $\alpha_b$ represents firm-level fixed effects, which account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 66 -->

<a id="sec-56"></a>

#### (2) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.). In particular, the Board observed in the historical data series that the interest income on trading assets ratio responds positively to short-term rate increases. This relationship reflects the adjustment of the average yield in the portfolio to changing market interest rates. The Board has also observed in the historical data series that the ratio of income on trading assets responds positively to increases in the BBB Bond Yield Index spread. This relationship reflects the upward adjustment of average interest earnings on trading assets when financial conditions tighten.

Following the standard procedure for macroeconomic variable selection, the Board selected the 3-month Treasury yield and the spread of the BBB Bond Index Yield to the 10-year Treasury yield for this model. This group of variables exhibited the best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and did not produce model instability when re-estimated at different starting points. The addition of
<!-- page 67 -->

alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold.

The Board has observed that interest income on the trading assets achieved in previous periods is correlated with future outcomes. The regression model accounts for this relationship by including a Year AR term.

Firms have individual preferences for holding trading assets, which can vary in risk, origination date, underlying interest rate terms (e.g., fixed vs. variable), and duration. Consequently, average yields vary across firms, even after controlling for macroeconomic factors. The regression model includes firm-specific fixed effects to account for this fact. Additionally, recent changes in a firm’s portfolio holdings are captured by the rolling-window fixed effects.

<!-- Source PDF page 67 -->

<a id="sec-57"></a>

#### (3) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity in the response of the dependent variable to changes in macroeconomic variables. For the interest income on trading assets model, coefficients on macroeconomic variables reflect average historical portfolio yield as interest rates and corporate credit spreads change. The model also assumes that all firms react equally to changes in the macroeconomic variables included in the regression. Increases in the Treasury rate or in the BBB credit spread will result in higher interest income for all firms at the same rate. Note that the inclusion of firm level and rolling-window fixed effects is not related to this issue. Fixed effects are related to the average level of the dependent variable over time, not to the sensitivity of the dependent variable to changes in macroeconomic variables.
<!-- page 68 -->

The Board understands that the linear regression model choice is appropriate and consistent with the Policy Statement principle of simplicity as it is considered at least as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

Another assumption in this model is that interest income on trading assets and interest expense from trading liabilities are independent of each other and are therefore modeled separately. However, the Board understands that firms could potentially report the underlying trading assets and liabilities or the corresponding income and expense components jointly. This reduces comparability across firms that could be introduced by differences in the extent of offsetting used in reporting trading assets and liabilities.

As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on a regression approach that models interest income and interest expense on trading assets and liabilities jointly. The Board proposes this approach of modeling a single net quantity rather than separate income and expense quantities to avoid challenges in cross-firm comparability that could be introduced by differences in the extent of offsetting used in reporting trading assets and liabilities.

<!-- Source PDF page 68 -->

<a id="sec-58"></a>

#### (4) Questions

*Question A32: The Board seeks comment on the regression model alternative that considers jointly interest income and expense on trading assets (net), as compared to the Board's current approach of using a single panel regression model for each component.*
<!-- page 69 -->

*Question A33: Is there any other alternative model that the Board should consider to project interest income on trading assets? What would be the advantages and disadvantages of using that alternative to project interest income on trading assets?*

*Question A34: Are there additional factors that the Board should consider in modeling interest income on trading assets? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A35: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest income on trading assets?*

*Question A36: Are there additional data sources the Board should consider incorporating in its modeling of interest income on trading assets? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 69 -->

<a id="sec-59"></a>

### h. All Other Interest Income

The series for all other interest income encompasses interest income streams that are not reported on the previously described interest income fields of the FR Y-9C. It includes: (1) income on real estate sales contracts reportable in Other Real Estate Owned; (2) interest income from advances to, or obligations of, majority-owned subsidiaries or associated companies; (3) interest received on other assets not specified in previous components; and (4) interest attributed to transactions that are not directly associated with a balance sheet asset, such as the interest attributed to interest rate swaps or to foreign exchange transactions.[^25]
<!-- page 70 -->

Since there is not a specific balance that corresponds to this income flow, the dependent variable used in this model regression is the ratio of this income normalized by the balance of total interest earning assets. Total interest earning assets are defined as the sum of total loans and leases, federal funds sold in domestic offices, securities purchased under agreements to resell, total mortgage-backed securities, interest bearing balances, and trading assets.[^26] The Board has chosen this definition of total interest earning assets for normalization because it has observed through statistical analysis that it is generally correlated with the amount of all other interest income. This correlation has been shown to be sufficient in order to avoid non-stationarity of the ratio that is used as the dependent variable in the regression. As is well recognized in statistics, non-stationarity in the time series of the dependent variable is an undesirable characteristic for a regression model. A regression model with a nonstationary dependent variable is subject to spurious correlation (in case any of the independent variables is also nonstationary) and can also lead to forecasts which are explosive in nature. By choosing an appropriate variable for normalization, the Board avoids the undesirable issue of non-stationarity in the regression model.

The Board observed in the historical data series that all other interest income is comprised of a wide range of interest incomes not accounted for in the previously discussed components, notably interest income on margin loans, non-trading derivatives, dividend income on Reserve Bank and FHLB stock, and income from fluctuations in interest rates. Hence, there is significant diversity across firms related to the underlying business activities that generate all other interest income.
<!-- page 71 -->

<!-- Source PDF page 71 -->

<a id="sec-60"></a>

#### (1) Model Specification

In the all other interest income regression model, the projected ratio is correlated solely with the average level of the ratio for each bank, both in the long run (through fixed effects) and during the year of lift-off (through the autoregressive coefficient). Projections are not correlated with macroeconomic variables.

The model is specified according to the following equation:

**Equation A9** – All Other Interest Income Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where:*

- $Ratio(b,t) = \frac{\text{all other interest income}_{b,t}}{\text{total interest earning assets balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $\alpha_b$ represents firm-level fixed effects, which accounts for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 71 -->

<a id="sec-61"></a>

#### (2) Variable Selection

Following the standard procedure for macroeconomic variable selection, the Board did not find a statistically significant, constant relationship, over the available time series and across all firms, between the ratio of all other interest income and the macroeconomic variables that are part of the stress test scenario. The lack of a constant and statistically significant relationship could be likely due to the diversity of business activities that generate income for this component. The regression, thus, does not include any macroeconomic variable as an independent variable.
<!-- page 72 -->

The regression includes firm-fixed effects and the Year AR term. Rolling firm-level fixed effects account for level heterogeneity and reflect the long-run average ratio for each bank. The Year AR term is included to capture the observed relationship between previous performance of the dependent variable and future outcomes.

<!-- Source PDF page 72 -->

<a id="sec-62"></a>

#### (3) Assumptions and Limitations

A limitation of the current model on all other interest income is that the dependent variable is not impacted by macroeconomic variables. The projected ratio thus converges to its long-run average, which is firm-specific, but is not stressed under the scenario. Alternative modeling options could increase data collection (at a more granular level) in order to build more detailed models; however, these options would increase the regulatory burden on firms.

The Board understands that the current regression model for all other interest income to be appropriate given the behavior of the underlying variables and consistent with the Policy Statement principle of simplicity. The Board considers this model to be as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

Structural model alternatives could also be used to model all other interest income. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on the structural approach. The Board proposes to model interest income from interest-bearing balances and interest income on other interest/dividend-bearing assets using a structural model framework and FR Y-14Q, Schedule G data. Using FR Y-14Q data allows the Board to identify all remaining interest-earning assets and as a result this
<!-- page 73 -->

component is subsumed into the models of interest income from interest-bearing balances and interest income on other interest/dividend-bearing assets.

<!-- Source PDF page 73 -->

<a id="sec-63"></a>

#### (4) Questions

*Question A37: The Board seeks comment on the structural model alternative that uses FR Y-14Q data, as compared to the Board's current approach of using a panel regression model.*

*Question A38: Are there any alternatives the Board should consider to the use of total interest earning assets balances as the denominator in the calculation of the ratio that enters the regression as dependent variable in this model? What are the advantages or disadvantages of these alternatives?*

*Question A39: Is there any other alternative model that the Board should consider to project all other interest income? What would be the advantages and disadvantages of using that alternative to project all other interest income?*

*Question A40: Are there additional factors that the Board should consider in modeling all other interest income? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A41: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of all other interest income?*

*Question A42: Are there additional data sources the Board should consider incorporating in its modeling of all other interest income? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*
<!-- page 74 -->

<!-- Source PDF page 74 -->

<a id="sec-64"></a>

### i. Regression Models for Interest Expense

The Board models four of the six interest expense components in the pre-provision net revenue model suite using the panel regression framework. The first three components represent deposit funding expenses and are:

- interest expense on domestic time deposits,
- interest expense on other domestic deposits, and
- interest expense on foreign deposits. The fourth component represents a combination of wholesale funding sources, namely:
- interest expense on trading liabilities, other borrowed money and all other interest expense.

In accordance with criteria previously described in Section A.ii.a.(1) Justification for the Use of Regression Models, the Board has determined that these four components are well-suited for the regression framework because they:

- are reported consistently across firms and over time in FR Y-9C, with a long time series of data available for model estimation; and
- are responsive to macroeconomic factors (typically to interest rate levels), and this relationship is statistically strong and economically significant.

Furthermore, the regression models for interest expense have generally provided good out-of-sample performance during model selection tests, specifically for periods of economic distress, and high in-sample fit.

The Board models two interest expense components using the structural approach, since the Board determined that they are less appropriate for the regression framework. These components are interest expense on federal funds purchased and securities sold under the agreements to repurchase, and interest expense on subordinated debt. For the former, the Board verified that a structural model is appropriate because there is homogeneity regarding liability
<!-- page 75 -->

composition, as well as a clear economic relationship between expected expenses, the liability balances of each firm, and the expected path of the interest rate. For the latter, a structural model is appropriate because there is heterogeneity in firms’ holdings of financial instruments but well-defined relationships between contracted financial instruments, expected expenses, and the path of the interest rate under the scenario. These two components are described later in Section A.iv.m. dedicated to structural models.

<!-- Source PDF page 75 -->

<a id="sec-65"></a>

#### (1) Interest Expense on Domestic Time Deposits

Interest expense on domestic time deposits is reported as interest expense on domestic time deposits of \$250,000 or less plus time deposits of more than \$250,000. The dependent variable used in this model regression is the ratio of this expense normalized by the balance of domestic time deposits.[^27]

Domestic time deposits are fixed at an interest rate for a set term before they can be withdrawn without penalty. The rate banks offer on time deposits often tracks the federal funds rate or the 3-month Treasury yield closely as short-term rates reflect the opportunity cost for investors in time deposits. While the use of time deposits fluctuates with interest rates (it is typically lower when interest rates are falling and higher when interest rates rise), time deposits are generally considered a stable source of funding.

<!-- Source PDF page 75 -->

<a id="sec-66"></a>

##### (a) Model Specification

In the interest expense on domestic time deposits model, the projected ratio is correlated with U.S. Treasury rates and the average level of the ratio for each firm.

The model is specified according to the following equation:
<!-- page 76 -->

**Equation A10** – Interest Expense on Domestic Time Deposits Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 Treasury3m(t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where:*

- $Ratio(b,t) = \frac{\text{interest expense in domestic time deposits}_{b,t}}{\text{domestic time deposits balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;
- $\alpha_b$ represents firm-level fixed effects, which account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 76 -->

<a id="sec-67"></a>

##### (b) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.). In particular, the Board observed in the historical data series that the interest expense on domestic time deposits ratio responds positively to short-term interest rate increases. This relationship reflects higher average costs of funding as the market risk-free rate moves upward and is frequently denominated “deposit beta.” The converse is true for decreases in the interest rate.

Following the standard procedure for macroeconomic variable selection, the Board selected the 3-month Treasury yield as the macroeconomic variable for use in this model. This variable demonstrated the best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and did not show signs of model instability when re-estimated at different starting points. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold.
<!-- page 77 -->

The Board has observed in historical data that as market interest rates move during an economic cycle, the average funding cost for time deposits is expected to follow. However, the adjustment is not immediate and depends on the origination date and the duration of current time deposits and on other factors (see Flannery and James (1984),[^28] for example). The regression model accounts for the relationship between previous performance of the dependent variable and future outcomes by including a Year AR term.

Finally, firms tend to face average long-run funding costs for time deposits that reflect their individual business models. The regression model accounts for this by including firm fixed effects. Recent changes in firms’ business models are captured by the rolling-window fixed effects.

<!-- Source PDF page 77 -->

<a id="sec-68"></a>

##### (c) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity and symmetry in the response of the dependent variable to changes in macroeconomic variables. For the domestic time deposits model, coefficients on the 3-month Treasury yield reflect the average historical deposit beta. As the component sums domestic time deposits of both large denominations with lower (time deposits of more than \$250,000 and those lower than that threshold), a related assumption is that the average historical deposit beta is sufficient to project interest expenses under stress. The model also assumes that all firms react equally to changes in the macroeconomic variables included in the regression. For this component, this assumption implies that the deposit beta is the same across firms. Note that the inclusion of firm level and rolling-window fixed effects is not related to this issue. Fixed effects are related to the
<!-- page 78 -->

average level of the dependent variable over time, not to the sensitivity of the dependent variable to changes in macroeconomic variables.

Alternative modeling options within the regression framework, such as non-linear models or interactions, could offer more flexibility to address asymmetrical responses. Models with asymmetrical deposit betas that depend on the direction of the interest rate change present a trade-off: they are typically able to provide more conservative projections for funding costs under rising interest rate scenarios when compared to simple linear models but tend to produce funding costs projections that are less conservative under low interest rate scenarios.

Further alternative modeling options within the regression framework could allow for, given a change in interest rates, different adjustments in deposit expenses across firms (heterogeneity) based on characteristics of their funding mix or on their business models. This option requires a relatively long time series of historical data for every firm to assure low variance in regression estimates, which may not be appropriate for firms that are newer reporters.

The Board understands that the current regression model for interest expense on domestic time deposits is appropriate and consistent with the Policy Statement principle of simplicity and considers it as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

Structural model alternatives can be used to project interest expense on time deposits. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on the structural approach.
<!-- page 79 -->

<!-- Source PDF page 79 -->

<a id="sec-69"></a>

##### (d) Questions

*Question A43: The Board seeks comment on the structural model alternative to project interest expense on time deposits, as compared to the Board's current approach of using a panel regression model.*

*Question A44: Is there any other alternative model that the Board should consider to project interest expense on domestic time deposits? What would be the advantages and disadvantages of using that alternative to project interest expense on domestic time deposits?*

*Question A45: Are there additional factors that the Board should consider in modeling interest expense on domestic time deposits? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A46: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest expense on domestic time deposits?*

*Question A47: Are there additional data sources the Board should consider incorporating in its modeling of interest expense on domestic time deposits? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

*Question A48: Should the model explicitly account for different funding costs and heterogeneous deposit betas across firms to project interest expense on domestic time deposits? If so, how, and what are the advantages and disadvantages of these approaches?*
<!-- page 80 -->

*Question A49: Are there any nonlinearity concerns that should be addressed in projecting interest expense on domestic time deposits? What would be the advantages or disadvantages of addressing nonlinearity?*

<!-- Source PDF page 80 -->

<a id="sec-70"></a>

#### (2) Interest Expense on Other Domestic Deposits

Interest expense on other domestic deposits includes all other domestic non-time deposits defined as interest expense on all interest-bearing deposits in domestic offices, excluding time deposits of \$100,000 or more in domestic offices of subsidiary commercial banks and in domestic offices of other subsidiary depository institutions. The dependent variable used in this model regression is the ratio of this expense normalized by the balance of other domestic deposits.[^29]

Other domestic deposits are interest-bearing bank deposits which depositors can generally withdraw at any time. The rates offered on these deposits generally follow changes in short-term rates, typically the federal funds rate or the 3-month Treasury yield. Because depositors face no restrictions on withdrawal, demand deposits are usually more responsive to economic conditions, particularly shocks to short-term rates.

<!-- Source PDF page 80 -->

<a id="sec-71"></a>

##### (a) Model Specification

In the interest expense on other domestic deposits model, the projected ratio is correlated with U.S. Treasury rates and the average level of the ratio for each bank.

The model is specified according to the following equation:
<!-- page 81 -->

**Equation A11** – Interest Expense on Other Domestic Deposits Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 Treasury3m(t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where*

- $Ratio(b,t) = \frac{\text{interest expense in other domestic deposits}_{b,t}}{\text{other domestic deposits balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;
- $\alpha_b$ represents firm-level fixed effects, which accounts for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 81 -->

<a id="sec-72"></a>

##### (b) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.). In particular, the Board observed in the historical data series that the interest expense on other domestic deposits ratio responds positively to short-term rate increases. This relationship reflects higher average costs of funding as the market risk-free rate moves upward. The converse is true for decreases in the interest rate.

Following the standard procedure for macroeconomic variable selection, the Board selected the 3-month Treasury yield as the macroeconomic variable in this model. This variable demonstrated best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and did not show signs of model instability when re-estimated at different starting points. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold.
<!-- page 82 -->

The Board has observed that as market interest rates move during an economic cycle, the average funding cost for other domestic deposits is expected to follow. However, this adjustment is not immediate. The regression model accounts for the relationship between previous performance of the dependent variable and future outcomes by including a Year AR term.

Firms tend to face average long-run funding costs for other domestic deposits that reflect their individual business models. The projections calculated by the regression model account for this by including firm fixed effects. Recent changes in firms’ business models are captured by the rolling-window fixed effects.

<!-- Source PDF page 82 -->

<a id="sec-73"></a>

##### (c) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity and symmetry in the response of the dependent variable to changes in macroeconomic variables. For the other domestic deposits model, coefficients on the 3-month Treasury yield reflect the average historical deposit beta. Another assumption of the model is that all firms react equally to changes in the macroeconomic variables included in the regression. For this component, this assumption implies that the deposit beta is the same across firms. Note that the inclusion of firm-level and rolling-window fixed effects is not related to this issue. Fixed effects are related to the average level of the dependent variable over time, not to the sensitivity of the dependent variable to changes in macroeconomic variables.

Alternative modeling options within the regression framework, such as non-linear models or interactions, could offer more flexibility to address asymmetrical responses. Models with asymmetrical deposit betas that depend on the direction of the interest rate change present a trade-off: they typically provide more conservative projections for funding costs under rising
<!-- page 83 -->

interest rate scenarios when compared to simple linear models but tend to provide less conservative funding costs projections under low interest rate scenarios.

Further alternative modeling options within the regression framework could allow for, given a change in interest rates, different adjustments in deposit expenses across firms (heterogeneity) based on characteristics of their funding mix or on their business models. This option requires a relatively long time series of historical data for every firm to assure low variance in regression estimates, which presents issues for firms that are newer to the sample.

The Board understands that the current regression model for interest expense on other domestic deposits is appropriate and consistent with the Policy Statement principle of simplicity, and considers it as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

Structural model alternatives can be used to project interest expense on other domestic deposits. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on the structural approach.

<!-- Source PDF page 83 -->

<a id="sec-74"></a>

##### (d) Questions

*Question A50: The Board seeks comment on the structural model alternative to project interest expense on other domestic deposits, as compared to the Board's current approach of using a panel regression model.*

*Question A51: Should the Board consider using a model that explicitly accounts for asymmetry in deposit betas instead of the current regression model? What would be the*
<!-- page 84 -->

*advantages and disadvantages of using a model that explicitly accounts for asymmetry in deposit betas to project interest expense on other domestic deposits?*

*Question A52: Are there other nonlinearity concerns that should be addressed in the current regression model used to project interest expense on other domestic deposits? If so, how, and what would be the advantages or disadvantages of doing so?*

*Question A53: Is there any other alternative model that the Board should consider to project interest expense on other domestic deposits? What would be the advantages and disadvantages of using that alternative to project interest expense on other domestic deposits?*

*Question A54: Are there additional factors that the Board should consider in modeling interest expense on other domestic deposits? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A55: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest expense on other domestic deposits?*

*Question A56: Are there additional data sources the Board should consider incorporating in its modeling of interest expense on other domestic deposits? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

*Question A57: Would including additional deposit characteristics as independent variables in the regression model, such as the average size of deposit accounts or other information regarding the deposit base, improve deposit beta estimates (consistent with the*
<!-- page 85 -->

*predictive model for deposit betas in Hirtle and Plosser [2025])?*[^30] *Are there any advantages or disadvantages of including these additional variables to project interest expense on other domestic deposits?*

*Question A58: Should the regression model for interest expense on other domestic deposits account for different expected deposit betas across firms? If so, how, and what would be the advantages or disadvantages of doing so? What are firm characteristics that are likely correlated with expected deposit betas? What are possible technical solutions that could be suggested to approach nonlinearity in this context? What would be the advantages or disadvantages of these solutions?*

<!-- Source PDF page 85 -->

<a id="sec-75"></a>

#### (3) Interest Expense on Foreign Deposits

Interest expense on foreign deposits is comprised of interest expense on all deposits in foreign offices included in the interest-bearing deposits in foreign offices, edge and agreement subsidiaries, and IBFs line item. This component also includes premiums paid or discounts received on foreign exchange contracts related to financial swap transactions that involve deposits in foreign offices. Such gains or losses are known at the inception of the contract and should be amortized over the life of the contract. The dependent variable used in this model regression is the ratio of this expense normalized by the balance of total foreign deposits.[^31]

<!-- Source PDF page 85 -->

<a id="sec-76"></a>

##### (a) Model Specification

In the interest expense on foreign deposits model, the projected ratio is correlated with U.S. Treasury rates and the average level of the ratio for each bank.
<!-- page 86 -->

The model is specified according to the following equation:

**Equation A12** – Interest Expense on Foreign Deposits Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 Treasury3m(t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where*

- $Ratio(b,t) = \frac{\text{interest expense in foreign deposits}_{b,t}}{\text{foreign deposits balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;
- $\alpha_b$ represents firm-level fixed effects, which account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 86 -->

<a id="sec-77"></a>

##### (b) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.). In particular, the Board observed in the historical data series that the interest expense on foreign deposits ratio responds positively to short-term rate increases. This relationship reflects higher average costs of funding as the U.S. market risk-free rate moves upward. The converse is true for decreases in the interest rate.

Following the standard procedure for macroeconomic variable selection, the Board selected the 3-month Treasury yield as the macroeconomic variable for this model. This variable demonstrated best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and did not show signs of model instability when re-estimated at different starting points. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold.
<!-- page 87 -->

The Board has observed that as market interest rates move during an economic cycle, the average funding cost for foreign deposits is expected to follow. However, the adjustment is not immediate. The regression model accounts for the relationship between previous performance of the dependent variable and future outcomes by including a Year AR term.

Firms tend to face average long-run funding costs for foreign deposits that reflect their individual business models. The regression model accounts for this by including firm fixed effects. Recent changes in firms’ business models are captured by the rolling-window fixed effects.

<!-- Source PDF page 87 -->

<a id="sec-78"></a>

##### (c) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity and symmetry in the response of the dependent variable to changes in macroeconomic variables. For the foreign deposits model, coefficients on the 3-month Treasury yield reflect the average historical deposit beta. Another assumption of the model is that all firms react equally to changes in the macroeconomic variables included in the regression. For this component, this implies that the deposit beta is the same across firms. Note that the inclusion of firm-level and rolling-window fixed effects is not related to this issue. Fixed effects are related to the average level of the dependent variable over time, not to the sensitivity of the dependent variable to changes in macroeconomic variables.

Alternative modeling options within the regression framework, such as non-linear models or interactions, could offer more flexibility to address asymmetrical responses. Models with asymmetrical deposit betas that depend on the direction of the interest rate change present a trade-off: they are typically able to provide more conservative projections for funding costs
<!-- page 88 -->

under rising interest rate scenarios when compared to simple linear models but provide less conservative funding rate projections under low interest rate scenarios.

Further alternative modeling options within the regression framework could allow for, given a change in interest rates, different adjustments in deposit expenses across firms (heterogeneity) based on the characteristics of their funding mix or on their business models. This option requires a relatively long time series of historical data for every firm to assure low variance in regression estimates, which pose issues for newer firms to the sample.

The Board understands that the current regression model for interest expense on foreign deposits is appropriate and consistent with the Policy Statement principle of simplicity, and considers it at least as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

Structural model alternatives can be used to project interest expense on foreign deposits. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on the structural approach.

<!-- Source PDF page 88 -->

<a id="sec-79"></a>

##### (d) Questions

*Question A59: The Board seeks comment on the structural model alternative to project interest expense on foreign deposits, as compared to the Board's current approach of using a panel regression model.*

*Question A60: Is there any other alternative model that the Board should consider to project interest expense on foreign deposits? What would be the advantages and disadvantages of using that alternative to project interest expense on foreign deposits?*
<!-- page 89 -->

*Question A61: Are there additional factors that the Board should consider in modeling interest expense on foreign deposits? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A62: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest expense on foreign deposits?*

*Question A63: Are there additional data sources the Board should consider incorporating in its modeling of interest expense on foreign deposits? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

*Question A64: Would the regression model for interest expense on foreign deposits benefit from explicitly accounting for asymmetry in deposit betas? If so, how should the regression model do so? What would be the advantages or disadvantages of these approaches? Are there other nonlinearity concerns that should be addressed to project interest expense on foreign deposits? If so, how, and what would be the advantages or disadvantages of doing so?*

*Question A65: Should the regression model for interest expense on foreign deposits account for different expected deposit betas across firms? If so, how, and what would be the advantages or disadvantages of doing so? Which firm characteristics are likely correlated with expected deposit betas? What are possible technical solutions that could address nonlinearity? What are the advantages or disadvantages of these solutions?*
<!-- page 90 -->

<!-- Source PDF page 90 -->

<a id="sec-80"></a>

#### (4) Interest Expense on Trading Liabilities, Other Borrowed Money and All Other Interest Expense

Trading liabilities and other borrowed money represent a significant portion of bank wholesale funding, and it is generally a more expensive liability than retail deposits. It is an important source of funding when deposits are under pressure. Banks may pay a fixed rate, correlated with the federal funds rate, on short-term debt or commercial paper, or they may pay the federal funds rate plus a premium in other cases like for margin loans or long-term debt. Larger banks historically rely more on wholesale funding than their smaller counterparts (this is empirically demonstrated for example by Choi and Choi [2021]).[^32] All other interest expense includes expenses paid on cash collateral in brokerage accounts and expenses on equity lending.

The Board determined that projecting these two sources of interest expense in a single component was appropriate because the Board’s statistical analysis demonstrated that both sources of interest expense exhibit comparable responses to changes in macroeconomic conditions.[^33] In this context, comparable means that the two sources of interest expense generally respond similarly (same sign, comparable magnitude) to the same macroeconomic variables.

Interest expense on trading liabilities and other borrowed money includes interest expense on commercial paper, mortgage indebtedness, and obligations under capitalized leases. All other interest expense includes interest on cash collateral, payables under securities loan agreements, and changes in rates on deposit accounts. The dependent variable used in this model
<!-- page 91 -->

regression is the ratio of this total expense normalized by the balance of trading liabilities and other borrowed money.[^34]

<!-- Source PDF page 91 -->

<a id="sec-81"></a>

##### (a) Model Specification

The Board projects this component using panel regressions. The regression specifications differ according to whether a firm has higher concentration of trading liabilities and other borrowed money balances. Following the procedures described in Section A.ii.a.(3), the Board empirically verified that the related expenses for banks with higher concentrations of these balances respond, on average, differently to changes in macroeconomic conditions than banks with lower concentrations. Thus, banks were classified in two different groups, large and small, based on their concentrations and correlation with other firms. The “large” and “small” naming convention was chosen to represent the groups since firms with large concentrations are also on average larger in size, measured as total assets.

The large group model is specified according to the following equation:

**Equation A13** - Interest Expense on Trading Liabilities, Other Borrowed Money and All Other

Interest Expense, Large Group Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 Treasury3m(t) + \beta_2 VIX(t) + \beta_3 VIXsq(t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where:*

- $Ratio(b,t) = \frac{\text{interest expense in trading liabilities, other borrowed money and all other}_{b,t}}{\text{trading liabilities and other borrowed money balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;
- $VIX(t)$ is the U.S. Market Volatility Index (VIX), representing general market risk;

<!-- page 92 -->

- $VIXsq(t)$ is the U.S. Market Volatility Index (VIX) squared, representing non-linear sensitivity to general market risk;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

The small group model is specified according to the following equation:

**Equation A14** – Interest Expense on Trading Liabilities, Other Borrowed Money and All Other Interest Expense, Small Group Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 Treasury3m(t) + \beta_2 Unemp(t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where:*

- $Ratio(b,t) = \frac{\text{interest expense in trading liabilities, other borrowed money and all other}_{b,t}}{\text{trading liabilities and other borrowed money balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;
- $Unemp(t)$ is the unemployment rate, representing business cycle conditions;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 92 -->

<a id="sec-82"></a>

##### (b) Variable Selection

To select the independent variables in each of the regressions, the Board used the standard procedure for macroeconomic variable selection and regression specification, described in Section A.ii.a.(3)(c.). For each group, the variables included in the specifications above demonstrated the best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and, at the same time, did not show signs of model instability
<!-- page 93 -->

when re-estimated at different starting points. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold. The Board selected different macroeconomic variables for each group because different statistical relationships exist, in the underlying historical data and across firms, between shocks to macroeconomic conditions and adjustments in funding costs.

For the sake of clarity, note that the use of two groups and the use of firm fixed effects are different techniques aimed to address different empirical issues observed in the data. Groups are used to address heterogeneity in the sensitivity of the dependent variable to changes in macroeconomic variables. For instance, expenses for some firms may react faster and stronger to changes in interest rates (whenever changes occur). On the other hand, firm fixed effects are used to address different average levels of the dependent variable over time. For example, some firms may have higher average funding costs for the whole time series (independent of the business cycle phase).

For both the large and small groups, the Board observed in the historical data series that this component responds positively to short-term rate increases. This relationship reflects the passthrough from the U.S. risk-free rate to wholesale funding costs. The magnitude is larger for firms that are part of the small group.

<!-- Source PDF page 93 -->

<a id="sec-83"></a>

###### Large Group

For firms in the large group, the Board observed in the historical data series that this component also responds positively to increased market volatility. This relationship reflects the influence of market risk on the cost of wholesale funding. Periods of higher volatility and market risk imply a higher degree of uncertainty regarding economic outcomes, making credit more scarce and more expensive for banks.
<!-- page 94 -->

<!-- Source PDF page 94 -->

<a id="sec-84"></a>

###### Small Group

For firms in the small group, the Board observed in the historical data series that this component responds positively to the unemployment rate. This relationship reflects business cycle factors influencing the cost of funding. A higher unemployment rate is associated with recessionary periods, where credit is scarcer and more expensive due to higher credit spreads and worse expectations for economic performance.

<!-- Source PDF page 94 -->

<a id="sec-85"></a>

###### Other Variables

The Board has observed that the cost of wholesale funding adjusts for changes in market interest rates during the economic cycle, but the adjustment is not immediate — It will depend on the effective maturity of the current debt instruments as well as other non-observed factors. The regression model accounts for the relationship between previous performance of the dependent variable and future outcomes by including a Year AR term.

Firms tend to face average long-run funding costs for wholesale funding that reflect their business models. The projections calculated by the regression model account for this fact by including firm-level fixed effects. Recent changes in firms’ business models are captured by the rolling-window fixed effects.

<!-- Source PDF page 94 -->

<a id="sec-86"></a>

##### (c) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity in the response of the dependent variable to changes in macroeconomic variables. In more precise technical terms, this is referred to linearity in the parameters included in each regression, as opposed to fully nonlinear models. Following procedures for macroeconomic variable selection described in Section A.ii.a.(3)(c.), the Board selected two specific functional
<!-- page 95 -->

forms (two different transformations) for the VIX independent variable in the large group regression of this component: the levels of the variable (VIX) and the square of the variable (VIX[^2]). Statistical testing demonstrated that the inclusion of two functional forms (two transformations) provides better out-of-sample forecasting performance and is better able to capture the effect of economic stress, thus justifying higher complexity in this specific case. Although the independent variable enters in the squared form, the regression model is still linear in the parameters.

An additional assumption of the model is that all firms in the same group react equally to changes in the macroeconomic variables included in each regression. This implies that the coefficients in macroeconomic variables are the same for firms that are part of the same group. Following the standard procedures for regression specification described in the model framework Section A.ii.a.(3)(c.), the Board classified firms in two groups for this model. Thus, for the case of this component, the response to macroeconomic variables can have two different magnitudes (one per group), which already provides some degree of flexibility.

The Board believes that the linear regression model choice with two groups for this component is consistent with the Policy Statement principle of simplicity and considers it as conceptually sound as more complex alternatives. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

Another assumption in this model is that interest income on trading assets and interest expense from trading liabilities are independent of each other and are therefore modeled separately. However, the Board understands that firms could potentially report the underlying trading assets and liabilities or the corresponding income and expense components jointly. This
<!-- page 96 -->

reduces comparability across firms that could be introduced by differences in the extent of offsetting used in reporting trading assets and liabilities.

As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle. The Board proposes a regression approach to model a subset of this component corresponding to interest expense on trading liabilities as part of interest income and interest expense on trading assets. The Board is proposing this approach of modeling a single net quantity rather than separate income and expense quantities to avoid challenges in cross-firm comparability that could be introduced by differences in the extent of offsetting used in reporting trading assets and liabilities. The Board also proposes to model the remaining subset of interest expense on trading liabilities, other borrowed money, and all other interest expense as interest expense on other borrowing jointly with interest expense on subordinated debt using a structural approach.

<!-- Source PDF page 96 -->

<a id="sec-87"></a>

##### (d) Questions

*Question A66: The Board seeks comment on the alternative structural approach, as compared to the Board's current approach of using a panel regression model to project interest expense on trading liabilities, other borrowed money, and all other interest expense.*

*Question A67: Is there any other alternative model that the Board should consider to project interest expense on trading liabilities, other borrowed money, and all other interest expense? What would be the advantages and disadvantages of using that alternative to project interest expense on trading liabilities, other borrowed money, and all other interest expense?*

*Question A68: Are there additional factors that the Board should consider in modeling interest expense on trading liabilities, other borrowed money, and all other interest expense? If so, what are they? What data source could the Board use to incorporate those additional*
<!-- page 97 -->

*factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A69: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest expense on trading liabilities, other borrowed money, and all other interest expense?*

*Question A70: Are there additional data sources the Board should consider incorporating in its modeling of interest expense on trading liabilities, other borrowed money, and all other interest expense? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*
<!-- page 98 -->

<!-- Source PDF page 98 -->

<a id="sec-88"></a>

### j. Regression Models for Noninterest Income

There are six noninterest income components:

- trading revenue,
- income on service charges on deposits,
- income on net servicing fees,
- income from fiduciary income, insurance fees, and annuity fees,
- income from investment banking fees, and
- all other noninterest income.

The Board models the first five of the six noninterest income components listed above in the pre-provision net revenue model suite using the panel regression framework previously described. All other noninterest income is projected using a nonparametric approach as discussed in more detail later.

In accordance with criteria previously stated in Section A.ii.a.(1) Justification for the Use of Regression Models), the Board has determined that these five components are well-suited for the panel regression framework because they:

- are reported consistently across firms and over time in FR Y-9C, with a long time series of data available for model estimation; and
- are responsive to macroeconomic factors, and this relationship is statistically strong and economically significant.

Furthermore, the regression models for noninterest income have generally provided satisfactory out-of-sample performance during model selection tests, specifically for periods of economic distress, and high in-sample fit.

For the last component of noninterest income, the Board adopts an alternative approach to the regression model. The Board projects all other noninterest income using the nonparametric approach, because of the absence of clear statistical sensitivity to macroeconomic factors and heterogeneity in reporting across firms.
<!-- page 99 -->

<!-- Source PDF page 99 -->

<a id="sec-89"></a>

#### (1) Noninterest Income on Trading Revenue

Trading Revenue (BHCKA220) includes the net gain or loss from trading cash instruments and off-balance sheet derivative contracts (including commodity contracts) that have been recognized during the calendar year-to-date.[^35] The Board projects this component as the ratio of trading revenue normalized by the balance of trading assets. The Board models noninterest income from trading separately for large firms subject to the global market shock and other firms. The model for noninterest income from trading for large firms is further split into modeling income from trading activities in fixed income securities (i.e., income from trading U.S. Treasuries) separately from income from all other trading activities.

<!-- Source PDF page 99 -->

<a id="sec-90"></a>

##### (a) Model Specification

The Board specifies two regression models for large firms, and one regression model for small firms. The large firms models project, respectively, (1) trading revenue from fixed income, and (2) other trading revenue. The model for small firms projects total trading revenue. The regression models are described as follows:
<!-- page 100 -->

**Equation A15** - Noninterest Income on Trading Revenue, Large Firms, Fixed Income

Regression Model

$$\begin{aligned}Ratio\,FI(b,t) = {} & \rho \sum_{j=1}^{j=4}\frac{Ratio\,FI(b,t-j)}{4} \\ & + \beta_1 \frac{\left(BBBSpread10y(t) - BBBSpread10y(t-1)\right)}{\left(1 + BBByield(t-1)\right)} + \alpha_b + \delta_b \\ & + \phi Seasonal(t) + \varepsilon(b,t)\end{aligned}$$

*where:*

- $Ratio\,FI(b,t)$ is the share of trading revenue from fixed income trading using FR Y-14Q reported income relative to total trading assets;
- $\sum_{j=1}^{j=4}\frac{Ratio\,FI(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $BBBSpread10y(t)$ is spread of the BBB bond index to 10-year US Treasury yield in percent, which is scaled by 1+ the lag of the BBB yield, representing revaluation adjustments due to changes in the risk premium;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm;
- $Seasonal(t)$ represents seasonal quarterly indicator variables; and
- $\varepsilon(b,t)$ is the error term of the regression.

**Equation A16** - Noninterest Income on Trading Revenue, Large Firms, Non-Fixed Income Regression Model

$$Ratio\,NFI(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio\,NFI(b,t-j)}{4} + \alpha_b + \delta_b + \phi Seasonal(t) + \varepsilon(b,t)$$

*where:*

- $Ratio\,NFI(b,t)$ is the share of trading revenue from non-fixed income trading using FR Y-14Q reported income relative to total trading assets;
- $\sum_{j=1}^{j=4}\frac{Ratio\,NFI(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm;
- $Seasonal(t)$ represents seasonal quarterly indicator variables; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- page 101 -->

**Equation A17** - Noninterest Income on Trading Revenue, Small Firms Regression Model

$$Ratio(b,t) = \beta_1 Treasury3m(t) + \alpha_b + \delta_b + \phi Seasonal(t) + \varepsilon(b,t)$$

*where:*

- $Ratio(b,t)$ is the ratio of noninterest income from trading using FR Y-9C reported trading income relative to total trading assets;
- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm;
- $Seasonal(t)$ represents seasonal quarterly indicator variables; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 101 -->

<a id="sec-91"></a>

##### (b) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.), to select the variables in the regression specification for the trading revenue model for large firms subject to the global market shock (for trading income from fixed income securities and non-fixed income securities) and for small firms.

Large firms, subject to the global market shock, derive most of their noninterest income from trading in fixed income securities (i.e., bonds and Treasuries). The change in the BBB spread, normalized by the BBB yield, captures income earned from revaluations due to changes in the spread. Intuitively, to the extent that banks are taking fixed income positions that are unhedged against movement in the risk premium, this term captures revaluation adjustments due to normalized changes in the risk premium. This variable demonstrated best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and at the same time did not show signs of model instability when re-estimated at different starting points. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold.
<!-- page 102 -->

The Board found that trading revenue from non-fixed income activities (comprising income from trading equities and commodities) does not respond significantly to the inclusion of macroeconomic variables. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold. The most intuitive variables that can explain variation in equity- and commodity-related income are measures of overall stock market performance and stock market volatility. For instance, to the extent that firms are generating income from market-making activities, their income could be higher during times of high volatility when trading volumes soar. To the extent that firms take actual long or short positions that are unhedged, their income may be positively correlated with overall stock market performance. Empirically, however, coefficients on macroeconomic variables such as VIX, the Dow Jones index, or their transformations were not statistically significant. Intuitively, this lines up with banks mostly generating income from market-making activities that are independent from whether the market is increasing or declining as well as empirically independent from measures of market volatility.

For banks in the small group, trading revenues are not broken down between fixed and non-fixed income. Following standard procedures for macroeconomic variable selection, the Board found that the 3-month Treasury yield, representing the risk-free short-term rate, performs well in predicting trading revenues. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold.

Firms tend to have long-run average trading revenue that reflects their business models. The projections calculated by the regression model account for this fact by including firm-level fixed effects. Recent changes in firms’ business model are captured by the rolling-window fixed
<!-- page 103 -->

effects. The regression model for firms in both large and small groups also includes quarterly indicator variables to capture regular seasonal variation in trading revenues.

Following the standard procedure for model selection, the Year AR term showed statistical significance for both components of trading revenues and is included in both models. A Year AR term captures persistence in fixed and non-fixed income related activities. As a result, the projections for trading revenues for firms subject to the global market shock show persistence and slow response to changes in revaluations.

Following the standard procedure for model selection, the Year AR term did not show statistical significance in the regressions for the small group. Thus, the Year AR term is not included in this regression specification. As a consequence, the projections for trading revenues for firms not subject to the global market shock typically respond rapidly to changes in the short-term interest rate.

<!-- Source PDF page 103 -->

<a id="sec-92"></a>

##### (c) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity in the response of the dependent variable to changes in macroeconomic variables. For the trading revenue model, coefficients on the changes in the BBB spread for noninterest income from trading in fixed income securities for large firms and the 3-month Treasury rate for small firms reflect the average historical passthrough from changes in the price of risk in fixed income securities or the short rate overall to this revenue component.

Another assumption of the model is that all firms react equally to changes in the macroeconomic variables included in the regressions. For the firms in the large group, this implies that trading revenues from fixed income securities are less sensitive to changes in the BBB spread when the yield is higher (firms are exposed to revaluation adjustments for positions
<!-- page 104 -->

that are unhedged against movement in the risk premium). Large firms derive a relatively small portion of their trading revenues from non-fixed income securities and their revenues are persistent over time. Therefore, the model for the non-fixed income portion of trading revenues for the large firms does not have a macroeconomic variable as a predictor of future revenues. For small firms (firms not subject to the global market shock), the 3-month Treasury has been identified as a predictor of revenues. For this component for firms in the small group, when the yield on the 3-month Treasury is higher, firms earn higher trading revenues.

Finally, the Board assumes that trading revenues for large firms are persistent (the Year AR term is included in both model specifications for large firms). However, for firms not subject to the global market shock, the Board assumes that trading revenues are not persistent from one year to the next.

The Board believes that the linear regression model of noninterest income on trading revenue is consistent with the Policy Statement principle of simplicity and has found that the linear regression model choice is as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

An alternative approach is to model noninterest income on trading revenue utilizing information from firms’ projections. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on firms’ projections. The Board proposes a model of total noninterest income based on data reported in the FR Y-14A schedule and aggregate industry-level time series. The proposed model of total
<!-- page 105 -->

noninterest income includes the current model of noninterest income on trading revenue, together with the current models for other components of noninterest income.

In the instance where the Board does not adopt the proposed model in 2026, the Board is considering the following alternative approach of modeling noninterest income from trading revenue. This alternative regression model specification would include using one regression model for all firms (without the split between large and small firms) and not splitting models by lines of business. The alternative model would also use an alternative macroeconomic variable – the change in the natural logarithm of the Dow Jones index. This alternative macroeconomic variable proxies for the indirect relationship between trading revenues and market returns, consistent with the evidence documented in academic literature (Gebka, 2025; Falato, Iercosan, and Zikes, 2025; Lu and Wallen, 2024; Modig, Inanoglu, and Lynch, 2024).[^36] The Board is considering this alternative utilizing FR Y-9C pro forma data using a similar regression framework with firm-level and rolling-window fixed effects as in the current model but without the autoregressive term or seasonality indicators. This alternative specification is concise and robust against richer specifications and against distinct sub-sample periods, such as the 2008 financial crisis and the post-Volcker rule period.

<!-- Source PDF page 105 -->

<a id="sec-93"></a>

##### (d) Questions

*Question A71: The Board seeks comment on the alternative approach based on firm’s projections reported in FR Y-14A, as compared to the Board's current approach of using a panel regression model to project noninterest income from trading revenue.*
<!-- page 106 -->

*Question A72: Is there an alternative model that the Board should consider to estimate noninterest income from trading revenue? What would be the advantages and disadvantages of using that alternative to estimate noninterest income from trading revenue?*

*Question A73: Are there additional factors that the Board should consider in modeling noninterest income from trading revenue? If so, what are they? What data sources could the Board use to incorporate these additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating these additional factors?*

*Question A74: Within the current regression framework, should the Board consider adding or removing any variables from the noninterest income from trading revenue model specification? For example, the Board could consider using the change in the natural logarithm of the Dow Jones index instead of the current macroeconomic variable as an alternative to the current macroeconomic variables. Are there other variables that the Board should consider? What would be the advantages and disadvantages of adding or removing those variables? The current regression framework for large trading revenue model from fixed income instruments may interact with trading gains/losses for firms subject to the global market shock. Are there alternatives model specification that might address this interaction?”*

*Question A75: Within the current regression framework, should the Board consider any alternative or additional transformations of the variables in the noninterest income from trading revenue model specification? If so, which transformations? What would be the advantages and disadvantages of those transformations?*
<!-- page 107 -->

*Question A76: Should the Board consider modeling noninterest income from trading revenues for all firms jointly rather than splitting firms into large and small groups? What would be the advantages of this approach?*

*Question A77: Are there additional data items reported on the FR Y-9C or FR Y-14 forms that the Board should consider incorporating in its modeling of noninterest income from trading revenue? If so, which ones? What would be the advantages and disadvantages of such additional data items?*

*Question A78: Are there additional data sources the Board should consider incorporating in its modeling of noninterest income from trading revenue? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 107 -->

<a id="sec-94"></a>

#### (2) Noninterest Income on Service Charges on Deposits

Noninterest income on service charges on deposits includes all depositor charges, that is, fees for maintenance charges, minimum deposits balance, overwritten checks, and other charges. For this component, the Board projects the ratio of this income normalized by the balance of total deposits.[^37]

<!-- Source PDF page 107 -->

<a id="sec-95"></a>

##### (a) Model Specification

The model is specified according to the following equation:

**Equation A18** – Noninterest Income on Service Charges on Deposits Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 Treasury3m(t) + \alpha_b + \delta_b + \phi Seasonal(t) + \varepsilon(b,t)$$

<!-- page 108 -->

*where:*

- $Ratio(b,t) = \frac{\text{noninterest income on service charges on deposits}_{b,t}}{\text{total deposits balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm;
- $Seasonal(t)$ represents seasonal quarterly indicator variables; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 108 -->

<a id="sec-96"></a>

##### (b) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.). In particular, the Board observed in the historical data series that the income on service charges on deposits ratio responds positively to short-term rate increases. This relationship likely reflects higher deposit-fee costs for depositors whenever interest rates are higher. The channels that explain this relationship can be various. For example, during periods of higher interest rates, depositors which hold debt are likely paying higher monthly debt payments (e.g. mortgages, auto loans), leaving them with less cash on hand. This could then lead to higher incidence of overdraft fees (noninterest income on service charges on deposits for the firms) for these depositors.

Following the standard procedure for macroeconomic variable selection, the macroeconomic variable selected to be part of this model was the 3-month Treasury yield. This variable demonstrated the best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and at the same time did not show signs of model instability when re-estimated at different starting points. The addition of alternative macroeconomic
<!-- page 109 -->

variables did not increase out-of-sample forecasting performance by more than the defined threshold.

Firms tend to face average long-run income on service charges on deposits which reflect their business models. In this particular case, the incidence of service charges could be related to the types of consumers (depositors) that the firm attracts, or to its business strategy in terms of fees. The projections calculated by the regression model account for this fact (unobserved firm characteristics) by including firm fixed effects. Recent changes in firms’ business models are captured by the rolling-window fixed effects. For this particular model, quarterly indicator variables are included in the regression to capture regular seasonal variation in income.

<!-- Source PDF page 109 -->

<a id="sec-97"></a>

##### (c) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity in the response of the dependent variable to changes in macroeconomic variables. For the service charges on deposits model, coefficients on macroeconomic variables thus reflect average changes in income as interest rates vary. Another assumption of the model is that all firms react equally to changes in the macroeconomic variables included in the regression. Increases in the Treasury rate will result in higher noninterest income for all firms, at the same rate.

The Board understands that the linear regression model of noninterest income on service charges on deposits is appropriate and consistent with the Policy Statement principle of simplicity as it is considered as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.
<!-- page 110 -->

An alternative approach is to model noninterest income on service charges on deposits utilizing information from firms’ projections. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on firms’ projections. The Board proposes a model of total noninterest income based on data reported in the FR Y-14A schedule and aggregate industry-level time series. The proposed model of total noninterest income subsumes the current model of noninterest income on service charges on deposits, together with the current models for other components of noninterest income.

<!-- Source PDF page 110 -->

<a id="sec-98"></a>

##### (d) Questions

*Question A79: The Board seeks comment on the alternative approach based on firm’s projections reported in FR Y-14A, as compared to the Board's current approach of using a panel regression model to project noninterest income on service charges on deposits.*

*Question A80: Is there an alternative model that the Board should consider to project noninterest income on service charges on deposits? What would be the advantages and disadvantages of using that alternative to project noninterest income on service charges on deposits?*

*Question A81: Are there additional factors that the Board should consider in modeling noninterest income on service charges on deposits? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A82: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of noninterest*
<!-- page 111 -->

*income on service charges on deposits? If so, which ones? What would be the advantages and disadvantages of such additional data items?*

*Question A83: Are there additional data sources the Board should consider incorporating in its modeling of noninterest income on service charges on deposits? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 111 -->

<a id="sec-99"></a>

#### (3) Noninterest Income from Net Servicing Fees

Noninterest income from net servicing fees includes income from servicing rights as well as changes to the net present value of future servicing rights on mortgages and credit cards.[^38] The Board projects this component as the ratio of this income normalized by the balance of total servicing assets.

<!-- Source PDF page 111 -->

<a id="sec-100"></a>

##### (a) Model Specification

The model is specified according to the following equation:

**Equation A19** – Noninterest Income from Net Servicing Fees Regression Model

$$Ratio(b,t) = \beta_1 RealGDPpctChange(t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where*

- $Ratio(b,t) = \frac{\text{noninterest income on net servicing fees}_{b,t}}{\text{total servicing assets balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $RealGDPpctChange(t)$ is the annualized quarterly real GDP percent change, representing business cycle conditions;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- page 112 -->

<!-- Source PDF page 112 -->

<a id="sec-101"></a>

##### (b) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.). In particular, the Board observed in the historical data series that the income on net servicing fees ratio responds positively to real GDP growth, which means that business cycle conditions are directly associated with the intensity of servicing fees income. The channels that explain this relationship can be various. For example, higher economic growth typically leads to increased mortgage financing allowing banks to capture the corresponding servicing fees.

Following the standard procedure for macroeconomic variable selection, the macroeconomic variable selected to be part of this model was the annualized quarterly real GDP percentage change. This variable demonstrated best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios and at the same time did not show signs of model instability when re-estimated at different starting points. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold.

Following the standard procedure for regression specification, the Board observed that the dependent variable responds quickly to changes in economic conditions, showing a low degree of persistence, conditional on the macroeconomic variable included. Given the results from statistical testing, the autoregressive term was not included in this regression.

Firms tend to face average long-run income on servicing fees which reflect their business models. For instance, the incidence of servicing fees could be related to the types of consumers that the firm attracts, the types of products it prioritizes, or to its business strategy in terms of fee pricing. The projections calculated by the regression model account for this fact (unobserved
<!-- page 113 -->

firm characteristics) by including firm-level fixed effects. Recent changes in firms’ business models are captured by the rolling-window fixed effects.

<!-- Source PDF page 113 -->

<a id="sec-102"></a>

##### (c) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity in the response of the dependent variable to changes in macroeconomic variables. For the net servicing fees model, coefficients on macroeconomic variables thus reflect average changes in income as the real GDP growth rate varies. Another assumption of the model is that all firms react equally to changes in the macroeconomic variables included in the regression. Increases in the real GDP growth rate will result in higher noninterest income for all firms, at the same rate.

Alternative modeling options within the regression framework, such as non-linear models, could offer more flexibility to address asymmetrical responses and provide more conservative projection outcomes under stress. However, models with asymmetrical macroeconomic sensitivity, which depend on the direction of the real GDP change, present a trade-off. They could provide more conservative projections for noninterest income under scenarios of collapsed economic activity when compared to simple linear models. At the same time, they may introduce higher variance on projections across stress testing cycles as the regression model is re-estimated, given the lower statistical power of independent variables coefficients.

The Board understands that the current regression model for noninterest income from net servicing fees to be appropriate given the behavior of the underlying variables and consistent with the Policy Statement principle of simplicity and considers this model to be as conceptually sound as more complex alternatives within the regression framework. Internal performance
<!-- page 114 -->

testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

An alternative approach is to model noninterest income from net servicing fees utilizing information from firms’ projections. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on firms’ projections. The Board proposes a model of total noninterest income based on data reported in the FR Y-14A schedule and aggregate industry-level time series. The proposed model of total noninterest income subsumes the current model of noninterest income from net servicing fees, together with the current models for other components of noninterest income.

<!-- Source PDF page 114 -->

<a id="sec-103"></a>

##### (d) Questions

*Question A84: The Board seeks comment on the alternative approach based on firm’s projections reported in FR Y-14A, as compared to the Board's current approach of using a panel regression model to project noninterest income on net servicing fees.*

*Question A85: Is there any other alternative model that the Board should consider to project noninterest income on net servicing fees? What would be the advantages and disadvantages of using that alternative to project noninterest income on net servicing fees? Do these alternatives imply further data collection?*

*Question A86: Are there additional factors that the Board should consider in modeling noninterest income on net servicing fees? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*
<!-- page 115 -->

*Question A87: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of noninterest income on net servicing fees?*

*Question A88: Are there additional data sources the Board should consider incorporating in its modeling of noninterest income on net servicing fees? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

*Question A89: Changes in net servicing fees observed historically can be heavily skewed, that is, they can exhibit extreme outcomes if the present value of rights changes significantly as happened in the 2008 financial crisis. Is there a better way to capture the risk of large variations in net servicing fees income due to the occurrence of extreme negative economic events than the current regression model? What are the advantages and disadvantages of these solutions?*

*Question A90: Should the Board consider adding or removing any variables from the noninterest income on net servicing fees model specification? If so, which variables? What would be the advantages and disadvantages of adding or removing those variables?*

*Question A91: Should the Board consider any alternative or additional transformations of the variables in the noninterest income on net servicing fees model specification? If so, which transformations? What would be the advantages and disadvantages of those transformations?*

<!-- Source PDF page 115 -->

<a id="sec-104"></a>

#### (4) Noninterest Income from Investment Banking Fees

Noninterest income from investment banking fees consists of commissions from securities brokerage, underwriting fees, and venture capital revenue. The Board projects this component as the ratio of this income normalized by the balance of total assets.[^39]
<!-- page 116 -->

<!-- Source PDF page 116 -->

<a id="sec-105"></a>

##### (a) Model Specification

The Board specifies the regression model for the ratio of noninterest income from investment banking. The model is specified according to the following equation:

**Equation A20** – Noninterest Income from Investment Banking Fees, Large Group Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 VIXChange(t) + \beta_2 BBB10yChange(t) + \alpha_b + \delta_b + \phi Seasonal(t) + \varepsilon(b,t)$$

*where:*

- $Ratio(b,t) = \frac{\text{noninterest income on investment banking fees}_{b,t}}{\text{total assets balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $VIXChange(t)$ is the year over year change in the U.S. Market Volatility Index (VIX), representing general market risk;
- $BBBSpread10yChange(t)$ is the change in the spread of BBB Bond Index Yield to 10-year Treasury yield, representing changes in financial conditions;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm;
- $Seasonal(t)$ represents seasonal quarterly indicator variables; and
- $\varepsilon(b,t)$ is the error term of the regression.

**Equation A21** – Noninterest Income from Investment Banking Fees, Small Group Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 BBB10yChange(t) + \alpha_b + \delta_b + \varepsilon(b,t)$$

*where:*

- $Ratio(b,t) = \frac{\text{noninterest income on investment banking fees}_{b,t}}{\text{total assets balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;

<!-- page 117 -->

- $BBBSpread10yChange(t)$ is the change in the spread of BBB Bond Index Yield to 10-year Treasury yield, representing changes in financial conditions;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 117 -->

<a id="sec-106"></a>

##### (b) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.). In particular, the Board observed in the historical data series that the income from investment banking fees for large firms responds negatively to market volatility, which means that increased volatility reduces fee income that firms can generate from activities such as underwriting and mergers and acquisitions advisory services. Firms in both large and small groups respond negatively to changes in the BBB spread relative to the yield for the 10-year Treasury, suggesting that when financing conditions are tighter, banks generate less investment banking-related fee income.

Following the standard procedure for macroeconomic variable selection, the macroeconomic variable selected to be part of this model were the change in VIX for firms in the large group and changes in the BBB bond index yield relative to the 10-year Treasury yield for firms in both groups. These variables demonstrated the best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and at the same time did not show signs of model instability when re-estimated at different starting points. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold.
<!-- page 118 -->

The Board has observed that noninterest income from investment banking activities responds to changes in market volatility and financial conditions during the economic cycle, but the adjustment is not immediate. It depends on various non-observed factors. The regression model accounts for the relationship between previous performance of the dependent variable and future outcomes by including a Year AR term for both groups of firms.

Firms tend to face average long-run income on fees from investment banking activities which reflect their business models. For instance, the incidence of fees generated from investment banking activities could be related to the types of firms that a bank has established a relationship with, their overall deal flow, the types of products it prioritizes, or to its business strategy in terms of fee pricing and overall deal volume. The projections calculated by the regression model account for this fact (unobserved firm characteristics) by including firm-level fixed effects. Recent changes in firms’ business models are captured by the rolling-window fixed effects. The specification for large firms also includes seasonality indicators to account for fluctuations in deal volume that could be driven by seasonal factors.

<!-- Source PDF page 118 -->

<a id="sec-107"></a>

##### (c) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity in the response of the dependent variable to changes in macroeconomic variables. For investment banking fees for large firms the Board assumes that the overall market volatility as well as financing conditions reflect changes in banks’ ability to generate deal volume and therefore earn fee income. The Board assumes that as market volatility increases or financing conditions worsen, firms go through fewer deals, and banks earn lower investment banking fee income as a result. Another assumption of the model is that all firms react equally to changes in the macroeconomic variables included in the regression. Increases in VIX for firms in the large
<!-- page 119 -->

group or increases in financing costs for all banks decrease investment banking fee income for all firms at the same rate.

Alternative modeling options, such as non-linear models, could offer more flexibility to address asymmetrical responses and provide more conservative projection outcomes under stress. However, models with asymmetrical macroeconomic sensitivity, which depend on the direction of changes in volatility or costs of financing, present a trade-off. They could provide more conservative projections for noninterest income under scenarios of lower volatility when compared to simple linear models. At the same time, they may introduce higher variance on projections across stress testing cycles, as the regression model is re-estimated, given the lower statistical power of independent variables coefficients.

The Board understands that the current regression model for noninterest income from investment banking fees to be appropriate given the behavior of the underlying variables and consistent with the Policy Statement principle of simplicity and considers this model to be as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

An alternative approach is to model noninterest income from investment banking fees utilizing information from firms’ projections. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on firms’ projections. The Board proposes a model of total noninterest income based on data reported in the FR Y-14A schedule and aggregate industry-level time series. The proposed model of total noninterest income subsumes the current model of noninterest income from
<!-- page 120 -->

investment banking fees, together with the current models for other components of noninterest income.

In the instance where the Board does not adopt the proposed model, the Board is considering the following alternative approach of modeling noninterest income from investment banking fees. This model relies on the FR Y-9C pro forma data and follows a similar regression framework but with a simpler specification without the autoregressive term or seasonality indicators. The Board is also considering using fewer macroeconomic variables harmonized across the two groups, as well as possibly eliminating the group structure. The benefit of this alternative approach is increased simplicity and potentially improved stability of projections over time.

<!-- Source PDF page 120 -->

<a id="sec-108"></a>

##### (d) Questions

*Question A93: The Board seeks comment on the alternative approach based on firm’s projections reported in FR Y-14A, as compared to the Board's current approach of using a panel regression model to project noninterest income from investment banking fees.*

*Question A94: Is there an alternative model that the Board should consider to estimate noninterest income from investment banking fees? What would be the advantages and disadvantages of using that alternative to estimate noninterest income from investment banking fees?*

*Question A95: Within the current regression framework, should the Board consider using nonlinear models instead of the panel regression model? What would be the advantages and disadvantages of using nonlinear models to project noninterest income from investment banking fees?*
<!-- page 121 -->

*Question A96: Are there additional factors that the Board should consider in modeling noninterest income from investment banking fees? If so, what are they? What data sources could the Board use to incorporate these additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating these additional factors?*

*Question A97: Are there additional data sources the Board should consider incorporating in its modeling of noninterest income from investment banking fees? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

*Question A98: Should the Board consider adding or removing any variables from the noninterest income from investment banking fees model specification? If so, which variables? What would be the advantages and disadvantages of adding or removing those variables?*

*Question A99: Should the Board consider any alternative or additional transformations of the variables in the noninterest income from investment banking fees model specification? If so, which transformations? What would be the advantages and disadvantages of those transformations?*

*Question A100: Should the Board consider modeling noninterest income from investment banking fees using a model based on the volume of transactions (e.g., volume of deals). What would be the advantages and disadvantages of using this alternative model?*

*Question A101: Should the Board consider modeling noninterest income from investment banking fees for all firms jointly rather than splitting firms into large and small groups? What would be the advantages and disadvantages of this approach?*
<!-- page 122 -->

*Question A102: Are there additional data items reported on the FR Y-9C or FR Y-14 forms that the Board should consider incorporating in its modeling of noninterest income from investment banking fees? If so, which ones? What would be the advantages and disadvantages of such additional data items?*

<!-- Source PDF page 122 -->

<a id="sec-109"></a>

#### (5) Noninterest Income from Fiduciary Income and Insurance Banking Fees

Noninterest income from fiduciary income and insurance banking fees consists of income from fiduciary activities, fees and commissions from annuity sales, underwriting income from insurance and reinsurance activities, and income from other insurance activities. The Board projects this component as the ratio of this income normalized by the balance of total assets less trading assets.[^40]

<!-- Source PDF page 122 -->

<a id="sec-110"></a>

##### (a) Model Specification

The model is specified according to the following equation:

**Equation A22** – Noninterest Income from Fiduciary Income and Insurance Banking Fees

Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 VIXChange(t) + \alpha_b + \delta_b + \phi Seasonal(t) + \varepsilon(b,t)$$

*where:*

- $Ratio(b,t) = \frac{\text{noninterest income from fiduciary income and insurance banking fees}_{b,t}}{\text{total assets balances}_{b,t} - \text{trading assets balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $VIXChange(t)$ is the year over year change in the U.S. Market Volatility Index (VIX), representing general market risk;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;

<!-- page 123 -->

- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm;
- $Seasonal(t)$ represents seasonal quarterly indicator variables; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 123 -->

<a id="sec-111"></a>

##### (b) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.). In particular, the Board observed in the historical data series that the fiduciary income and insurance banking fees ratio responds negatively to changes in the U.S. market volatility index (VIX). This means that in times of increased market volatility and uncertainty, banks generate lower fee income from insurance and other fiduciary activities. The possible channels through which this relationship might manifest are that, in times of economic uncertainty and market volatility, fewer customers engage in reinsurance or annuity sales activities, resulting in lower fee income.

Following the standard procedure for macroeconomic variable selection, the macroeconomic variable selected to be part of this model was the year-on-year change in VIX. This variable demonstrated best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and at the same time did not show signs of model instability when re-estimated at different starting points. The addition of alternative macroeconomic variables did not increase out-of-sample forecasting performance by more than the defined threshold.

Following the standard procedure for regression specification, the Board observed that the dependent variable shows a high degree of persistence, conditional on the macroeconomic variable included. Given the results from statistical testing, the autoregressive term was included in this regression.
<!-- page 124 -->

Firms tend to face average long-run fiduciary and insurance banking fees income which reflect their business models. For instance, the incidence of insurance or reinsurance fees could be related to the types of customers that the firm attracts, the types of products it prioritizes, or to its business strategy in terms of fees’ pricing. The projections calculated by the regression model account for this fact (unobserved firm characteristics) by including firm-level fixed effects. Recent changes in firms’ business models are captured by the rolling-window fixed effects. The model specification also includes seasonality indicators to account for fluctuations in fee income that could be driven by seasonal factors.

<!-- Source PDF page 124 -->

<a id="sec-112"></a>

##### (c) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity in the response of the dependent variable to changes in macroeconomic variables. For the fiduciary income and insurance and banking fees model, coefficients on macroeconomic variables thus reflect average changes in fee income with changes in the overall U.S. market volatility. Another assumption of the model is that all firms react equally to changes in the macroeconomic variables included in the regression. Increases in the U.S. market volatility will result in lower noninterest income from fiduciary, insurance, and other banking activities for all firms, at the same rate.

Alternative modeling options, such as non-linear models, could offer more flexibility to address asymmetrical responses and provide more conservative projection outcomes under stress. However, models with asymmetrical macroeconomic sensitivity, which depend on the direction of VIX, present a trade-off. They could provide more conservative projections for noninterest income under scenarios of collapsed economic activity when compared to simple linear models. At the same time, they may introduce higher variance on projections across stress
<!-- page 125 -->

testing cycles, as the regression model is re-estimated, given the lower statistical power of independent variables coefficients.

The Board understands that the current regression model for noninterest income on fiduciary income and insurance and banking fees to be appropriate given the behavior of the underlying variables and consistent with the Policy Statement principle of simplicity and considers this model to be as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

An alternative approach is to model noninterest income on fiduciary income and insurance and banking fees utilizing information from firms’ projections. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on firms’ projections. The Board proposes a model of total noninterest income based on data reported in the FR Y-14A schedule and aggregate industry-level time series. The proposed model of total noninterest income subsumes the current model of noninterest income on fiduciary income and insurance and banking fees, together with the current models for other components of noninterest income.

<!-- Source PDF page 125 -->

<a id="sec-113"></a>

##### (d) Questions

*Question A103: The Board seeks comment on the alternative approach based on firms’ projections reported in FR Y-14A, as compared to the Board's current approach of using a panel regression model to project noninterest income from fiduciary income and insurance banking fees.*
<!-- page 126 -->

*Question A104: Regarding the current regression approach, should the Board consider using nonlinear models instead of the panel regression model? What would be the advantages and disadvantages of using nonlinear models to project noninterest income from fiduciary income and insurance banking fees?*

*Question A105: Is there any other alternative model that the Board should consider to project noninterest income from fiduciary income and insurance banking fees? What would be the advantages and disadvantages of using that alternative to project noninterest income from fiduciary income and insurance banking fees?*

*Question A106: Should the Board consider modeling noninterest income from fiduciary income and insurance banking fees jointly with noninterest income from investment banking fees? What would be the advantages and disadvantages of modeling these two components jointly?*

*Question A107: Are there additional factors that the Board should consider in modeling noninterest income from fiduciary income and insurance banking fees? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A108: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of noninterest income from fiduciary income and insurance banking fees?*

*Question A109: Are there additional data sources the Board should consider incorporating in its modeling of noninterest income from fiduciary income and insurance*
<!-- page 127 -->

*banking fees? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 127 -->

<a id="sec-114"></a>

### k. Regression Models for Noninterest Expense

The Board models the three noninterest expense components in the pre-provision net revenue model suite:

- compensation,
- fixed assets, and
- all other noninterest expense. The Board uses different model approaches for each component. Noninterest expense on compensation is modeled using the panel regression framework combined with an adjustment for variable pay expenses. Noninterest expense on fixed assets is modeled using the panel regression framework. All other noninterest expense is modeled using a nonparametric approach.

In accordance with criteria previously stated in Section A.ii.a.(1) Justification for the Use of Regression Models), the Board has determined that the two first components are well suited to the panel regression framework because they:

- are reported consistently across firms and over time in FR Y-9C, with a long time series of data available for model estimation; and
- are responsive to macroeconomic factors (typically to the level of interest rates), and this relationship is statistically strong and economically significant.

Furthermore, the Board has found that the panel regression models for noninterest expense generally provide good out-of-sample performance during model selection tests, specifically for periods of economic distress, and high in-sample fit.
<!-- page 128 -->

<!-- Source PDF page 128 -->

<a id="sec-115"></a>

#### (1) Noninterest Expense on Compensation

Noninterest expense on compensation is composed of salaries and benefits of all officers and employees of the firm and its consolidated entities. As with all the regression models for pre-provision net revenue, the dependent variable used in this model regression is a ratio. The ratio is the flow of noninterest expense on compensation (in dollars) normalized by the balance of total assets (in dollars as well).[^41]

<!-- Source PDF page 128 -->

<a id="sec-116"></a>

##### (a) Model Specification

The Board projects this component using panel regressions. Following the procedures for regression specification described in Section A.ii above, the Board empirically verified that compensation expenses for firms concentrated on traditional banking activities respond, on average, differently to changes in macroeconomic conditions than compensation expenses for firms engaged in more diverse activities (investment banking and trading). Firms engaged in more diverse activities, on average, respond more intensively to changes in financial market conditions than their peers and adjust compensation expenses accordingly. Some of these differences can be explained by differences in the firms’ revenue compositions. The Board observed in the historical data that firms with business models focused on traditional banking (e.g., deposits taking and lending) tend to have more stable compensation structures whereas firms that engage in more investment banking or trading activities tend to have compensation structures more responsive to changes in business performance. For example, some institutions link their compensation directly to their revenue streams.
<!-- page 129 -->

Using the methodology for regression specification, the Board classified firms in two different groups, large and small, based on their business model and correlation with other firms. The label “large” designates the group of firms highly engaged in investment banking or trading activities, which are usually also larger in size as measured by total assets, while the label “small” corresponds to the group of firms focused on traditional banking.

Following the general methodology for the regression specification, the Board estimates different regressions for each group (i.e., large and small). The specification of the regression equation is very similar for both groups. The only difference in the regression equation is that the model for large groups include seasonality variables. The independent macroeconomic variable, the Year AR term, the firm-level fixed effects and the rolling-window fixed effects are common in the specification for both groups.

The model for both groups is specified according to the following equation:

**Equation A23** – Noninterest Expense on Compensation Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \beta_1 BBBSpread10yChange(t) + \alpha_b + \delta_b + \phi Ind\left(large(b)\right) * Seasonal(t) + \varepsilon(b,t)$$

*where:*

- $Ratio(b,t) = \frac{\text{noninterest expense on compensation}_{b,t}}{\text{total assets balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $BBBSpread10yChange(t)$ is the change in the spread of BBB Bond Index Yield to 10-year Treasury yield, representing changes in financial conditions;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm;
- $Ind\left(large(b)\right) * Seasonal(t)$ represents seasonal quarterly indicator variables for firms which are part of the large group only; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- page 130 -->

<!-- Source PDF page 130 -->

<a id="sec-117"></a>

##### (b) Variable Selection

The Board used the standard procedure for macroeconomic variable selection and regression specification, described in Section A.ii.a.(3)(c.). In particular, the Board observed in the historical data series that compensation expenses are typically affected by financial markets conditions. Firms’ business models and revenue composition are factors which can explain how much compensation expenses vary over the business cycle. Compensation can be typically classified in two parts: fixed and variable. Fixed compensation refers to employee salaries and benefits, while variable compensation is comprised broadly of performance-based payouts. The Board has observed that the latter component of compensation expense is more prone to cyclical variations that depend on economic and financial markets conditions.

The Board observed in the historical data series that the noninterest expense from compensation ratio responds negatively to changes in the BBB spread, for banks in both groups. This relationship reflects tighter financial conditions (higher credit spreads) affecting negatively the performance of the banking business, thus implying lower compensation expenses as a ratio of total assets. The relationship is more pronounced for banks in the large group, suggesting that their expenses are more sensitive to firms’ performance.

Following the standard procedure for macroeconomic variable selection, the macroeconomic variable selected to be part of this model, for both large and small groups, was the change in the spread of BBB Bond Index Yield to 10-year Treasury yield. This variable demonstrated the best out-of-sample forecasting performance, provided macroeconomic sensitivity in stressed scenarios, and at the same time did not show signs of model instability when re-estimated at different starting points. The addition of alternative macroeconomic
<!-- page 131 -->

variables did not increase out-of-sample forecasting performance by more than the defined threshold.

The Board has observed that expenses in compensation respond to changes in financial conditions during the economic cycle, but the adjustment is not immediate. The regression model accounts for the relationship between previous performance of the dependent variable and future outcomes by including a Year AR term for both large and small groups.

Firms tend to face average long-run compensation costs which reflect their business models. The projections calculated by the regression model account for this fact by including firm-level fixed effects, for both large and small groups. Recent changes in firms’ business model are captured by the rolling-window fixed effects, also for both groups.

Following the standard procedure for regression specification, the Board verified that the historical data series for firms in the large group has a seasonal component. As a consequence, the regression model for firms in the large group has quarterly indicator variables to capture regular seasonal variation in compensation expenses.

<!-- Source PDF page 131 -->

<a id="sec-118"></a>

##### (c) Adjustment for Variable Compensation

Despite using the regression model with two groups to allow for variation in the sensitivity of projections to macroeconomic variables, the Board observed in the historical data that there was still significant heterogeneity in the large group regarding the magnitude of the response of compensation expenses to changes in macroeconomic factors. In particular, the Board observed that compensation expenses for some firms were more responsive to economic conditions, and this was correlated with a higher share of variable compensation. In order to better capture heterogeneity across firms, the Board implemented a model adjustment to explicitly condition the model projections on the share of variable compensation. This
<!-- page 132 -->

enhancement is intended to account for heterogeneity of business lines and compensation practices across firms.

The model adjustment uses data from the FR Y-14 reporting and is described in more detail below. The variable pay subcomponent of compensation is defined as the sum of cash, stock, and commissions, as reported in the FR Y-14.

A haircut, or proportional adjustment *H*, is defined based on the decline of variable pay expenses from firm projections in the FR Y-14A relative to recent historical expenses. This adjustment is applied based on each firm’s proportion of variable pay expenses to total compensation expenses reported in FR Y-14Q.

The adjusted total compensation expense projection, for each bank *i* in projection quarter *t*, is computed as follows:

**Equation A24** – Adjusted Total Compensation Expense Projection

$$\widehat{P_{i,t}} = (1 - q_i)P_{i,t}^{Fed} + q_i P_{i,t}^{Fed} H$$

In this equation, $P_{i,t}^{Fed}$ is the Board’s stress test projection for compensation (in dollars) for bank $i$ at projection quarter $t$, and $q_i$ is the share of variable pay expenses relative to total compensation for the past historical year for bank $i$, as reported in FR Y-14Q.

$$q_i = \frac{\sum_{t=Jumpoff\ Quarter-3}^{Jumpoff\ Quarter}\left(Expense_{i,t}^{VarPay}\right)}{\sum_{t=Jumpoff\ Quarter-3}^{Jumpoff\ Quarter} Expense_{i,t}^{Comp}}$$

The constant *H* represents a haircut to be applied to the variable pay share. The haircut is calculated as a ratio of two quantities:

- In the numerator, a stressed ratio for variable pay based on firms’ projections is defined as the ratio of average expenses from variable pay projected by all firms in the FR Y-14A

divided by the average expense on this category for the year prior to the start of the

projection horizon as reported in the FR Y-14Q.
<!-- page 133 -->

- In the denominator, a similar stressed ratio for total compensation based on firms’ projections is defined as the ratio of average compensation expenses projected by all

firms in the FR Y-14A, divided by the average expense in this category for the year prior

to the start of the projection horizon as reported in the FR Y-14Q.

The constant H, thus, can be written as:

$$H = \frac{StressedRatio^{VarPay}}{StressedRatio^{Comp}} = \frac{\dfrac{\frac{1}{8}\sum_{t=1}^{8}\left(Expense_t^{VarPay}\right)}{\frac{1}{4}\sum_{t=Jumpoff\ Quarter-3}^{Jumpoff\ Quarter}\left(Expense_t^{VarPay}\right)}}{\dfrac{\frac{1}{8}\sum_{t=1}^{8}Expense_t^{Comp}}{\frac{1}{4}\sum_{t=Jumpoff\ Quarter-3}^{Jumpoff\ Quarter}Expense_t^{Comp}}}$$

*H* is calculated for the aggregate industry. Expenses in the *H* equation are not indexed by bank *i*. *H* is calculated in the aggregate to avoid disparate treatment across banks; i.e.,

$$Expense_t^{VarPay} = \sum_i Expense_{i,t}^{VarPay}$$

$$Expense_t^{Comp} = \sum_i Expense_{i,t}^{Comp}$$

<a id="sec-119"></a>

##### (d) Assumptions and Limitations

Among assumptions and limitations previously discussed, the regression model assumes linearity in the response of the dependent variable to changes in macroeconomic variables. For the compensation expenses model, coefficients for the change in the BBB spread thus reflect average historical passthrough from financial conditions to expenses, for firms which are part of each group. An additional assumption of the regression model is that all firms in the same group react equally to changes in the macroeconomic variables included in each regression. This implies that the coefficients in scenario variables are the same for firms which are part of the
<!-- page 134 -->

same group. Following the standard procedures for regression specification described in Section A.ii above, the Board classified firms in two groups for this model. Thus, for the case of this component, the response to macroeconomic variables can have two different magnitudes (one per group), which already provides some degree of flexibility.

The haircut adjustment for variable compensation relies on the firm’s expense projections reported in FR Y-14A. As such, they are subject to specific criteria that were considered by each firm in developing its own internal models and methods. In addition, firms report projections in FR Y-14A only for a set of scenarios defined each cycle by the Board. In this sense, using firms’ projections limits internal analysis of additional scenarios by the Board, unless further assumptions are made.

The Board understands that the current regression model for noninterest expense on compensation with the haircut adjustment for variable compensation to be appropriate given the behavior of the underlying variables and consistent with the Policy Statement principle of simplicity. The Board considers this model to be as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on projecting a firm’s aggregate noninterest expense as a function of projected revenues (net interest income plus noninterest income) and the firm’s
<!-- page 135 -->

projected efficiency ratio.[^42] This alternative avoids the projection of components of noninterest expense separately, such as compensation and all other noninterest expense.

In the instance where the Board does not adopt the proposed model in 2026, the Board is considering the following alternative approach of modeling noninterest expense on compensation as a share of revenues. This alternative compensation model relies on the fundamental economic principle that firms aim to maximize profits by aligning compensation with employee productivity, both to manage costs effectively and to incentivize performance. In this framework, compensation expense tends to move with revenues for two reasons. First, when employees generate more revenue, they often expect — and firms are willing — to provide higher compensation. Second, firms use compensation not only to reward output but also as a tool to motivate continued performance. This link between revenue generation, cost control, and performance incentives forms the foundation of the alternative model, which relates compensation expenses to various revenue components.

However, this relationship is more complex in practice. For instance, revenue generated from a loan may take several years to materialize, with its ultimate value subject to fluctuation until maturity. Assessing future demand for financial services and determining whom to hire and how much to compensate them for their work to meet that demand adds further complexity. Moreover, many roles within banks support multiple business lines, such as cash management services, complicating the identification of a precise functional relationship between bank revenue and compensation. Additionally, compensation structures vary across different lines of business. Some may incur relatively fixed labor costs regardless of revenue, while others may
<!-- page 136 -->

explicitly tie wages to revenues to provide incentives. Therefore, the alternative model that the Board is considering aims to be sufficiently general to capture a wide range of potential relationships between revenue and total firm-level compensation that reflect the diversity of banking activities. This structure could yield more stable pre-provision net revenue projections, as higher revenues would be naturally offset by correspondingly higher compensation expenses.

This alternative model that the Board is considering would employ a panel regression framework to model bank compensation expenses as a function of various revenue streams. The framework is similar to the current regression framework but does not include an autoregressive term or groups. Specifically, the explanatory variables include interest income, trading revenue, fee income from fiduciary activities and investment banking, other noninterest income, interest expense, other noninterest expenses, and loan loss provisions. This alternative model also includes rolling-window fixed effects and a weighted least squares estimation. This model is estimated using historical pro forma data from FR Y-9C and is subsequently used to forecast compensation based on projected values of these explanatory variables. All variables on both sides of the regression are scaled by total revenue, defined as the sum of net interest income and noninterest income, minus all other noninterest income, calculated as a four-quarter rolling sum.

<!-- Source PDF page 136 -->

<a id="sec-120"></a>

##### (e) Questions

*Question A110: The Board seeks comment on the alternative approach based on firm’s projected efficiency ratio, as compared to the Board's current approach of using a panel regression model to project noninterest expense on compensation.*

*Question A112: Regarding the current model, should the Board use more than two groups of firms in the regression model for noninterest expense on compensation, and what would the trade-offs be to use a larger number of groups of banks?*
<!-- page 137 -->

*Question A113: Regarding the current approach, should the Board use only a panel regression model instead of a panel regression and the adjustment for variable compensation to project compensation expenses? What are the advantages and disadvantages of using the adjustment for variable compensation based on firms’ projections to calculate noninterest expense on compensation projections for stress testing?*

*Question A114: Are there other alternative modeling frameworks that the Board should consider to project noninterest expense from compensation? What would be the advantages and disadvantages of using these alternatives?*

*Question A115: The Board seeks comment on an alternative regression approach that would project compensation expenses as a function of various revenue streams, as compared to the Board's current regression approach to project noninterest expense on compensation.*

*Question A116: Are there additional data sources or items in regulatory reports (FR Y-9C or FR Y-14 forms) that the Board should consider incorporating in its modeling of noninterest expense on compensation? What are the advantages and disadvantages of such additional data items?*

*Question A117: Are there additional data sources the Board should consider incorporating in its modeling of noninterest expense on compensation? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

*Question A118: Should the Board use a different scaling variable, for example, revenues when computing ratios of noninterest expense on compensation? What would be other alternative scaling variables? What would be the advantages and disadvantages of using a different scaling variable when computing ratios of noninterest expense on compensation?*
<!-- page 138 -->

<!-- Source PDF page 138 -->

<a id="sec-121"></a>

#### (2) Noninterest Expense on Fixed Assets

Noninterest expense on fixed assets includes all noninterest expenses related to the use of premises, equipment, furniture, and fixtures. As with all the regression models for pre-provision net revenue, the Board projects this component as a ratio. The ratio is the flow of noninterest expense on fixed assets (in dollars) normalized by the balance of total assets (in dollars as well).[^43]

<!-- Source PDF page 138 -->

<a id="sec-122"></a>

##### (a) Model Specification

The model is specified according to the following equation:

**Equation A25** – Noninterest Expense on Fixed Assets Regression Model

$$Ratio(b,t) = \rho \sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4} + \alpha_b + \delta_b + \phi Seasonal(t) + \varepsilon(b,t)$$

*where:*

- $Ratio(b,t) = \frac{\text{noninterest expense on fixed assets}_{b,t}}{\text{total assets balances}_{b,t}}$ is the observed dependent variable of this regression for firm $b$ at quarter $t$;
- $\sum_{j=1}^{j=4}\frac{Ratio(b,t-j)}{4}$ is the Year AR term, which represents the average value of the dependent variable observed on the previous four quarters;
- $\alpha_b$ represents firm-level fixed effects, to account for heterogeneity in the average level of the ratio over time across firms;
- $\delta_b$ represents rolling-window fixed effects, which account for recent changes in the average level of the ratio for each firm;
- $Seasonal(t)$ represents seasonal quarterly indicator variables; and
- $\varepsilon(b,t)$ is the error term of the regression.

<!-- Source PDF page 138 -->

<a id="sec-123"></a>

##### (b) Variable Selection

The Board used the standard procedure for macroeconomic variable selection, described in Section A.ii.a.(3)(c.). In particular, the Board observed in the historical data series that the
<!-- page 139 -->

noninterest expense on fixed assets ratio is stable and acyclic, that is, there is no evidence that it fluctuates according to economic conditions.

Following the standard procedure for macroeconomic variable selection, the Board has not found a statistically significant constant relationship, over the available time series and across all firms, between the ratio of all other interest income and macroeconomic variables that are part of the stress test scenario. Thus, this model does not include any macroeconomic variables as independent variables in the regression.

The reasons for the absence of correlation between that expense stream and economic factors can be various. For example, even though better economic conditions may lead firms to expand their footprint, and thus, their fixed assets expenses, it will also lead them to expand their total assets. Since the dependent variable is the flow of expenses normalized by total assets, there will be no observed correlation between the dependent variable and macroeconomic variables.

Firms tend to face a fixed cost structure that reflects their business models. For example, banks with a large retail branch network are likely to face higher relative costs of fixed assets than banks which prefer to operate more intensively through digital platforms. The projections calculated by the regression model account for this fact (unobserved heterogeneity at firm level) by including firm-level fixed effects. Recent changes in firms’ business models are captured by the rolling-window fixed effects.

The regression model accounts for the relationship between previous performance of the dependent variable and future outcomes by including a Year AR term. Seasonality is statistically observed for this component, so quarterly indicator variables are included in the regression. The reason for the occurrence of seasonality is likely related to the concentration of some large fixed-
<!-- page 140 -->

expense items in a specific quarter of the year. For instance, most property taxes must be paid at specific months, and this is likely true for other large items.

<!-- Source PDF page 140 -->

<a id="sec-124"></a>

##### (c) Assumptions and Limitations

The model assumes no relationship between projections and macroeconomic variables in the scenario. The projections are thus not stressed by the scenario, and the projected ratios converge to bank-specific long-run averages.

The Board understands that the current regression model for noninterest expense on fixed assets to be appropriate given the behavior of the underlying variables and consistent with the Policy Statement principle of simplicity and considers this model to be as conceptually sound as more complex alternatives within the regression framework. Internal performance testing exercises have demonstrated that the model is sufficiently able to capture the effect of economic stress as it has shown satisfactory out-of-sample fit.

As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on projecting a firm’s aggregate noninterest expense as a function of projected revenues (net interest income plus noninterest income) and the firm’s projected efficiency ratio.[^44] This alternative avoids the projection of components of noninterest expense separately, such as noninterest expense on fixed assets.
<!-- page 141 -->

<!-- Source PDF page 141 -->

<a id="sec-125"></a>

##### (d) Questions

*Question A119: The Board seeks comment on the alternative approach based on firm’s projected efficiency ratio, as compared to the Board's current approach of using a panel regression model to project noninterest expense on fixed assets.*

*Question A120: Should the Board consider alternative models to project noninterest expense on fixed assets under stress test scenarios? What are the advantages and disadvantages of any such alternatives? Do these alternatives imply further data collection?*

*Question A121: Are there additional factors that the Board should consider in modeling noninterest expense on fixed assets? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A122: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of noninterest expense on fixed assets?*

*Question A123: Are there additional data sources the Board should consider incorporating in its modeling of noninterest expense on fixed assets? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 141 -->

<a id="sec-126"></a>

### l. Estimated Parameters of Regression Models

The tables included in this section present the estimated parameters (coefficients) for all regression models in the pre-provision net revenue suite. The parameters presented in the tables are the ones used for the calculation of projections for the 2025 stress test. Included in the tables are, for each model:
<!-- page 142 -->

- the autocorrelation estimated coefficients;
- the independent macroeconomic variables estimated coefficients;
- bank-specific covariates estimated coefficients; and
- seasonality indicator estimated coefficients.

Estimated coefficients for firm fixed effects are not included in the tables.

**Table A4**| - Estimated Parameters for Regression Models on Interest Income and Interest Expense Components|

| Component | Year AR | 3M Treasury Yield | 3M Treasury Yield Lag | Term Spread, Percent (t10y-t3m) | Term Spread Lag, Percent (t10y-t3m) | Term Spread, Percent (t5y-t3m) | Spread of BBB Bond Index to 10 Year Treasury Yield in Percent | Other |
|---|---|---|---|---|---|---|---|---|
| **Interest Income Models** | | | | | | | | |
| Loans | 0.636*** | 0.345*** | | | 0.116*** | | | Credit Card Loans/Total Loans (%): 0.035*** |
| Interest Bearing Balances | 0.395*** | 0.760*** | | | 0.146* | | | |
| US Treasuries | 0.574*** | 0.395*** | | | | 0.145** | | |
| Mortgage Backed Securities | 0.688*** | | 0.202*** | | | | | |
| Other Securities | | 0.805*** | | 0.588*** | | | 0.355*** | |
| Federal Funds and Repo | | | | | | | | |
| Trading Assets | 0.543*** | 0.161*** | | | | | 0.083*** | |
| All Other | 0.779*** | | | | | | | |
| **Interest Expense Models** | | | | | | | | |
| Domestic Time Deposits | 0.611*** | 0.358*** | | | | | | |
| Other Domestic Deposits | 0.487*** | 0.255*** | | | | | | |
| Foreign Deposits | 0.430*** | 0.461*** | | | | | | |
| Federal Funds and Repo | | | | | | | | |
| Trading + OBM + All Other (Large) | 0.449*** | 0.403*** | | | | | | US Market Volatility Index: 0.0005; US Market Volatility Index^2: -0.00001 |
| Trading + OBM + All Other (Small) | 0.566*** | 0.450*** | | | | | | Unemployment rate: 0.113*** |

<!-- page 143 -->

**Table A5** - Estimated Parameters for Regression Models on Noninterest Income and Noninterest Expense Components|

| Component | Year AR | 3 Month Treasury Yield | Year over Year change in VIX | Change in Spread of BBB Bond Index to 10 Yr. Treasury Yield in Percent | Ch. in BBB Spread / (1 + Lag BBB) | Annualized Quarterly Real GDP Percent Change | Seasonality Indicators |
|---|---|---|---|---|---|---|---|
| **Noninterest Income** | | | | | | | |
| Fiduciary Income and Insurance Fees | 0.792*** | | -0.0003*** | | | | Q1: 0.002; Q2: 0.009; Q3: -0.006 |
| Net Servicing Fees | | | | | | 0.601** | |
| Service Charges on Deposits | 0.932*** | 0.009*** | | | | | Q1: -0.012; Q2: 0.007; Q3: 0.016* |
| Investment Banking Fees (Large) | 0.833*** | | -0.001** | -0.071*** | | | Q1: -0.024; Q2: -0.001; Q3: -0.044*** |
| Investment Banking Fees (Small) | 0.664*** | | | -0.018*** | | | |
| Trading Revenue (Small) | | 0.723*** | | | | | Q1: 1.099**; Q2: 1.041**; Q3: 0.274 |
| Trading - FI (Large) | 0.519*** | | | | -3.918*** | | Q1: 3.082***; Q2: 2.048**; Q3: 1.170 |
| Trading - NFI (Large) | 0.493*** | | | | | | Q1: 1.173***; Q2: 0.519***; Q3: 0.226 |
| **Noninterest Expense** | | | | | | | |
| Compensation (Large) | 0.885*** | | | -0.081*** | | | Q1: 0.085***; Q2: 0.031**; Q3: -0.016 |
| Compensation (Small) | 0.899*** | | | -0.028*** | | | |
| Fixed Assets | 0.938*** | | | | | | Q1: -0.016***; Q2: -0.020***; Q3: -0.017*** |

<!-- page 144 -->

<!-- page 145 -->

<!-- Source PDF page 145 -->

<a id="sec-127"></a>

### m. Structural Models

The Board models three interest income and expense components using structural models. They are:

- interest income from federal funds sold and securities purchased under agreements to resell
- interest expense from federal funds purchased and securities sold under agreements to repurchase
- interest expense on subordinated debt In accordance with criteria previously stated in Section A.iv.m. Structural Models, the Board observed for these components a well-defined relationship between contracted financial instruments or balances for each firm at lift-off date, the expected income or expense flow, and the expected path of the interest rate. Thus, the Board has determined that these components are well suited to structural models.

<!-- Source PDF page 145 -->

<a id="sec-128"></a>

#### (1) Interest Income from Federal Funds Sold and Securities Purchased under Agreements to Resell

Interest income from federal funds sold and securities purchased under agreements to resell consists of interest earned on funds sold or lent to another financial institution. Most of these securities have short durations and are directly linked to short-term interest rates. The relevant balances for this component are the assets underlying federal funds sold and securities purchased under the agreement to resell.[^45]

The Board applies a structural approach to model interest income from this component because it has observed in historical data that the income responds directly and rapidly to
<!-- page 146 -->

movements in short-term interest rates. In addition, the Board considers this component relatively homogeneous in composition, both within and across firms.

<!-- Source PDF page 146 -->

<a id="sec-129"></a>

##### (a) Model Description

Under this structural approach, interest income for this component at each quarter of projection is calculated starting from a simple and intuitive assumption: income flow for a portfolio can be defined as the product of the rate earned times the balances.

More formally, let *Fb* be the income earned on federal funds sold and securities purchased under the agreement to resell for firm *b*, *Bb* be the associated asset balance, and *rb* be the rate that the firm earns on this balance:[^46]

**Equation A26** – Interest Income from Federal Funds Sold and Securities Purchased under Agreements to Resell|

$$F_{b,t} = r_{b,t}B_{b,t}$$

This equation states that the flow of income for a given period $t$ is the product of the balance times the interest rate (yield) earned by the firm.

Using this equation for the projection period, the projected flow of income $F_{b,q}$, for firm $b$ in quarter $q$ on the projection horizon, thus, can be calculated as:

$$F_{b,q} = r_{b,q}B_{b,q}$$

The stress test assumes constant balances for all firms, then $B_{b,q} = B_{b,q0}$ for all periods, where $q0$ represents the lift-off quarter. This means that the projected flow of income is going to be calculated based on the balances at the start of the projection horizon.

The remaining term that needs to be defined to calculate projected flows is $r_{b,q}$, or the yield earned by each firm $b$ in each projection quarter $q$. The Board assumes that this yield responds directly to short-term interest rates, as this is consistently observed in historical data. In particular, the Board assumes that the yield $r_{b,t}$ (at any time period *t*) is proportional to the 3-month U.S. Treasury rate $Treasury3m_t$, as this is a representative short-term interest rate.|

<!-- page 147 -->

Based on this proportionality assumption, let $k_{b,t}$ be defined as:

$$k_{b,t} = \frac{r_{b,t}}{Treasury3m_t}$$

which is a scalar that represents the yield each firm earns relative to the 3-month U.S. Treasury rate. Rearranging terms, $r_{b,t} = k_{b,t}Treasury3m_t$.

The Board assumes that, for the projection horizon, the scalar $k_{b,q}$ will be constant for each firm and equal to the scalar at the lift-off quarter. This implies $k_{b,q} = k_b$, where $b$ is observed at lift-off quarter.

Clarifying and using previous definitions, $k_b$ at lift-off (quarter 0) is calculated as a function of the reported interest income on the component, the balances, and the 3-month U.S. Treasury rate all at the lift-off quarter:

$$k_i = \frac{r_{b,0}}{Treasury3m_0} = \frac{F_{b,0}}{B_{b,0}Treasury3m_0}$$

So, the equation used to project the flow of income $F_{b,q}$ can be written as:

$$F_{b,q} = r_{b,q}B_{b,q} = k_{b,q}Treasury3m_q B_{b,q} = k_b Treasury3m_q B_b,$$

*where:*

- $k_b$ is computed for each firm $b$ as a function of the reported interest income on the component, the balances, and the 3-month U.S. Treasury rate at the lift-off quarter;
- $B_b$ are the observed balances at lift-off for each firm $b$; and
- $Treasury3m_q$ is the scenario path for the 3-month U.S. Treasury rate for a given quarter $q$.

<!-- page 148 -->

<!-- Source PDF page 148 -->

<a id="sec-130"></a>

##### (b) Assumptions and Limitations

As discussed above, when using the structural model the Board makes the following assumptions to calculate income projections: the yield each firm earns over the projection horizon is proportional to the 3-month U.S. Treasury rate; this proportion is fixed for each bank; and this proportion is equal to the proportion observed at the lift-off quarter.

The Board considered using alternative modeling approaches for this component, such as panel regressions. The Board determined that the structural model described above had several advantages over a panel regression framework, including enhanced clarity and explainability as well as simplicity; for example, it does not involve coefficient estimation. In addition, structural models avoid statistical estimation, meaning that the variability of projections over stress testing cycles can be fully explained by reported income and balances for each bank.

As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on a structural model. The Board proposes a structural model for interest income on other interest/dividend-bearing assets, which includes interest income earned on federal funds sold and securities purchased under agreements to resell. The proposed model is conceptually similar to the current model, but benefits from using FR Y-14Q-reported balances. Using FR Y-14Q-reported balances allows the Board to project interest income on this component directly.

<!-- Source PDF page 148 -->

<a id="sec-131"></a>

##### (c) Questions

*Question A124: The Board seeks comment on the structural model alternative that uses data from FR Y-14Q reported balances, as compared to the Board's current approach to project interest income on federal funds sold and securities purchased under agreements to resell.*
<!-- page 149 -->

*Question A125: Are there other alternative models that the Board should consider to project interest income on federal funds sold and securities purchased under agreements to resell? What are advantages and disadvantages of these alternatives?*

*Question A126: Are there additional factors that the Board should consider in modeling interest income on federal funds sold and securities purchased under agreements to resell? What data sources could the Board use to incorporate these additional factors?*

*Question A127: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest income on federal funds sold and securities purchased under agreements to resell?*

*Question A128: Are there additional data sources the Board should consider incorporating in its modeling of interest income on federal funds sold and securities purchased under agreements to resell? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 149 -->

<a id="sec-132"></a>

#### (2) Interest Expense on Federal Funds Purchased and Securities Sold under the Agreements to Repurchase

Interest expense on federal funds purchased and securities sold under agreements to repurchase consists of interest expense on funds purchased or borrowed from another financial institution.[^47] Most of these securities have short durations and are directly linked to short-term interest rates. The relevant balances for this component are the liabilities underlying federal funds purchased and securities sold under the agreement to repurchase.[^48]
<!-- page 150 -->

The Board applies a structural approach to model interest expense from this component because it has observed in historical data that the expense flow responds directly and rapidly to movements in short-term interest rates. In addition, this component is relatively homogeneous in composition, both within and across firms.

<!-- Source PDF page 150 -->

<a id="sec-133"></a>

##### (a) Model Description

The structural approach to calculating projections for interest expense on federal funds purchased and securities sold under agreements to repurchase is equivalent to the one previously described for interest income on federal funds sold and securities purchased under agreements to resell. For the sake of completeness, it is summarized below.

Under this structural approach, interest expense for this component at each quarter of projection is calculated starting from a simple and intuitive assumption: expense flow for a portfolio can be defined as the product of the rate paid times the balances.

More formally, let *Fb* be the expense paid on federal funds purchased and securities sold under agreements to repurchase for firm *b*, *Bb* be the associated asset balance, and *rb* be the rate that the firm earns on this balance:

**Equation A27** – Interest Expense on Federal Funds Purchased and Securities Sold under the Agreements to Repurchase|

$$F_{b,t} = r_{b,t}B_{b,t}$$

This equation states that the flow of expense for a given period $t$ is the product of the balance times the interest rate paid by the firm. Using this equation for the projection period, the projected flow of expense $F_{b,q}$, for firm $b$ in quarter $q$ on the projection horizon, thus, can be calculated as:

$$F_{b,q} = r_{b,q}B_{b,q}$$

<!-- page 151 -->

The stress test assumes constant balances for all firms; therefore, $B_{b,q} = B_{b,q0}$ for all periods, where $q0$ represents the lift-off quarter. This means that the projected flow of expense is going to be calculated based on the balances at the start of the projection horizon.

The remaining term that needs to be defined in order to calculate projected flows is $r_{b,q}$, or the rate paid by each firm $b$ in each projection quarter $q$. The Board assumes that this rate responds directly to short-term interest rates, as this is consistently observed in historical data. In particular, the Board assumes that the rate $r_{b,t}$ (at any time period $t$) is proportional to the 3-month U.S. Treasury rate $Treasury3m_t$, as this is a representative short-term interest rate.

Based on this proportionality assumption, let $k_{b,t}$ be defined as:

$$k_{b,t} = \frac{r_{b,t}}{Treasury3m_t}$$

which is a scalar that represents the rate each firm pays relative to the 3-month U.S. Treasury rate. Rearranging terms, $r_{b,t} = k_{b,t}Treasury3m_t$.

The Board assumes that, for the projection horizon, the scalar $k_{b,q}$ will be constant for each firm and equal to the scalar at the lift-off quarter. This implies $k_{i,q} = k_i$, where $k_i$ is observed at lift-off quarter.

Clarifying and using previous definitions, $k_b$ at lift-off (quarter 0) is calculated as a function of the reported interest expense on the component, the balances, and the 3-month U.S. Treasury rate all at the lift-off quarter:

$$k_b = \frac{r_{b,0}}{Treasury3m_0} = \frac{F_{b,0}}{B_{b,0}Treasury3m_0}$$

So, the equation used to project the flow of expense $F_{i,q}$ can be written as:

$$F_{b,q} = r_{b,q}B_{b,q} = k_{b,q}Treasury3m_q B_{b,q} = k_b Treasury3m_q B_b,$$

*where:*

<!-- page 152 -->

- $k_b$ is computed for each firm $b$ as a function of the reported interest expense on the component, the balances, and the 3-month U.S. Treasury rate at the lift-off quarter;
- $B_b$ are the observed balances at lift-off for each firm $b$; and
- $Treasury3m_q$ is the scenario path for the 3-month U.S. Treasury rate for a given quarter $q$.

<!-- Source PDF page 152 -->

<a id="sec-134"></a>

##### (b) Assumptions and Limitations

As previously mentioned, when using the structural model the Board makes the following assumptions to calculate expense projections: the rate each firm pays over the projection horizon is proportional to the 3-month U.S. Treasury rate; this proportion is fixed for each bank; and this proportion is equal to the proportion observed at the lift-off quarter.

Alternative modeling approaches could use panel regressions, as adopted in other models of pre-provision net revenue. Advantages of the structural model when compared to regression models are enhanced clarity and explainability. In addition, variability of projections over stress testing cycles can be fully explained by reported expense and balances for each bank as structural models avoid statistical estimation.

As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on a structural model. The Board proposes a structural model for interest expense on federal funds purchased and securities sold under the agreement to repurchase using a similar but simpler approach based on data reported in FR Y-14Q. Using FR Y-14Q reported balances allows the Board to project interest expense on this component directly.
<!-- page 153 -->

<!-- Source PDF page 153 -->

<a id="sec-135"></a>

##### (c) Questions

*Question A129: The Board seeks comment on the structural model alternative that uses data reported in FR Y-14Q to project interest expense on federal funds purchased and securities sold under agreements to repurchase, as compared to the Board's current approach.*

*Question A130: Are there other alternative models that the Board should consider to project interest expense on federal funds purchased and securities sold under agreements to repurchase? What are advantages and disadvantages of these alternatives?*

*Question A131: Are there additional factors that the Board should consider in modeling interest expense on federal funds purchased and securities sold under agreements to repurchase? What data sources could the Board use to incorporate these additional factors?*

*Question A132: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest expense on federal funds purchased and securities sold under agreements to repurchase?*

*Question A133: Are there additional data sources the Board should consider incorporating in its modeling of interest expense on federal funds purchased and securities sold under agreements to repurchase? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 153 -->

<a id="sec-136"></a>

#### (3) Interest Expense on Subordinated Debt

Subordinated debt notes are term-structured financial instruments (e.g., bonds) that are subordinated to deposits and any other liabilities. These bond types became a significant source of funding following the 2008 financial crisis (Acharya et al., 2011).[^49] Interest expense on
<!-- page 154 -->

subordinated debt is broadly defined as the interest expense on outstanding notes and debentures and is reported on the FR Y-9C.[^50]

The Board projects interest expense on subordinated debt using a structural model that relies on security-level data for individual positions reported in the FR Y-14Q.[^51] The Board also relies on vendor data for credit ratings and missing data as well as reference rates from the macroeconomic scenario and the appropriate Treasury and corporate bond yields as projected by the Yield Curve Model.[^52]

<!-- Source PDF page 154 -->

<a id="sec-137"></a>

##### (a) Model Description

The Board calculates interest expense on subordinated debt as the outstanding balance multiplied by the contractual rate for each debt security, adjusted to account for unamortized costs from subordinated debt issued at a premium or discount and to account for interest rate hedging through swap agreements.

Maturing debt is assumed to be refinanced using new debt with similar characteristics on the first day of the quarter. Generally, the total subordinated debt expense for each firm at projection quarter *t*, indexed by instrument *i,* is calculated as:[^53]
<!-- page 155 -->

**Equation A28** – Interest Expense on Subordinated Debt Projection

$$Total\ Subdebt\ Expense_t = \sum_i Interest\ Expense_{i,t} + \sum_i Amortization_{i,t} + \sum_i Swap\ Adjustment_{i,t}$$

In this manner, supervisory projections align with the accrual-based reporting standards of subordinated debt expenses in FR Y-9C line item BHCK4397.

The interest expense term in the subordinated debt model is based on the contractual coupon rate for fixed, floating, and variable debt, and is calculated for each firm-quarter as follows:

$$Interest\ Expense_{i,t} = Coupon\ Rate_{i,t} \times Notional\ Amount_{i,t}$$

where the coupon rate depends on the type (fixed, floating, step-up, or variable) and maturity (whether the debt matures before or after the forecast horizon) of each underlying subordinated debt security[^54].

In addition to using the contractual terms to determine interest expense, the Board makes assumptions about how debt is replaced upon maturity that reflects the heightened costs of rolling over debt during a crisis. Interest expense is calculated for each instrument type as follows, using coupon rates and spreads over index from the FR Y-14Q:

1. Fixed-rate securities: The security pays a fixed rate equal to the level of the scenario-consistent corporate yield curve projections. When fixed-rate debt matures over the forecast horizon, it is refinanced with fixed-rate debt of the same maturity. The coupon rate of the new security is determined based on the yield curve in the scenario plus a credit spread that reflects the rating of the firm. The firm’s credit rating is constant in the base case and downgraded two notches in the severely adverse case. The decision to downgrade firms’ credit ratings in the severely adverse scenario is consistent with history, since it aligns with observed facts during the 2008 financial crisis. In this way, the model captures the potential risk that borrowing costs increase for firms.
<!-- page 156 -->

2. Floating-rate securities: Coupon rates are calculated as the sum of spread over index, where the index rate is the rate reported at issuance. The Board uses lagged scenario rates to forecast interest expense on floating rate debt, because the frequency of rate resets is not fully aligned with the rates in the contemporaneous quarter. The Board assumes that floating rate debt is refinanced with debt of the same maturity tied to the same reference rate as the original security. The spread of the replacement bond is a function of the spread of the maturing bond and the change in the credit rating of the firm between the initial bond issuance and the current date. The firm’s credit rating is constant in the base case and downgraded two notches in the severely adverse case. The decision to downgrade firms’ credit ratings in the severely adverse scenario is consistent with history, since it aligns with observed facts during the 2008 financial crisis.

3. Step-up securities: Several firms have issued securities that step up or convert from paying a fixed rate to paying a floating rate. This security type receives the coupon at issuance for the first leg and the coupon rate when terms change. The Board assumes that step-up securities with a variable rate are refinanced with debt of the same maturity and rating (downgraded two notches in the severely adverse scenario), but that they pay a fixed coupon consistent with the scenario corporate yields.

4. Convertible securities: This security type receives the coupon at issuance for the first leg, and, when terms change, the coupon rate is calculated as the sum of spread over index. The Board assumes that convertible securities with a variable rate are refinanced with debt of the same maturity and rating (downgraded two notches in the severely adverse scenario) but that they pay a fixed coupon consistent with the scenario corporate yields.

Explicitly, the spread of the security that is issued at time *t* and replaces a security with a rating *r* and maturity *m* is calculated as follows:

$$\begin{aligned}spread_{r_{scenario},m,t} = {} & spread_{maturing} + \left(corp\_yield_{r_{scenario},m,t} - ref\_rate_{t-1}\right) \\ & - \left(corp\_yield_{r,m,t} - ref\_rate_{t-m-1}\right)\end{aligned}$$

*where:*

- $spread_{maturing}$ is the reported spread on the maturing security;
- $corp\_yield_{r,m,t}$ is the yield on the corporate bond with a credit rating $r$ and maturity $m$ at time $t$;
- the second term in the equation above measures the change in the spread of a maturity- and rating-matched corporate bond between the original issuance date of the maturing bond and the forecast quarter; and
- the term $r_{scenario}$ reflects the rating of the new, replacing security that depends on the scenario (same as maturing bond in base case scenario and two notches downgrade in the severely adverse scenario).

Changes in the spread reflect changes in the price of risk between the issuance date of the original security and refinancing date as well as changes in the credit rating of the firm. To
<!-- page 157 -->

implement the above formula, the Board requires historical information on corporate yield curves and reference rates. Quarterly historical yield curves and quarterly historical reference rates are auxiliary variables and utilize publicly available and vendor-based data.[^55]

The amortization term in the subordinated debt model is calculated as a linear depreciation of the FR Y-14Q-reported balance of unamortized premiums or discounts over the life of the security.[^56]

$$Amortization_i = \frac{-Unamortized\ amount_i \times \left(Scenario\ Start\ Quarter - Issue\ date_i\right)}{Total\ number\ of\ quarters\ until\ maturity_i}$$

Only securities on the balance sheet at the start of the projection horizon are subject to amortization. Securities that are modeled as a replacement of maturing securities during the forecast horizon are assumed to be issued at par (i.e., not at a premium or a discount) and therefore do not require amortization.

Banks may engage in swaps that change the cost of subordinated debt from the contractual terms. The most prevalent swap is an interest rate swap that changes fixed-rate coupons to a variable-rate expense. The Board estimates exposure to interest rate swaps on a bank-by-bank basis using an adjustment term. The swap adjustment term in the subordinated debt model relies on unamortized values and notional swap amounts. Specifically, the Board infers the subordinated debt expense attributable to floating rate swaps by backing out the expense related to the unhedged fixed-rate or floating-rate notes and amortization in the last historical quarter. For each bank *b*:
<!-- page 158 -->

$$Swap\ Expense_b = \underbrace{Total\ Subordinated\ debt\ Expense_b}_{from\ FR\,Y\text{-}9C} - \underbrace{Interest\ Expense\ on\ Unhedged\ Notes_b}_{\sum_i Interest\ Expense_{i,t}^{\,Unhedged}} - \sum_i Amortization_{i,b}$$

The portion of hedged versus unhedged notes is based on the data provided by firms on the FR Y-14Q. The Board calculates the implied annual spread over the most common index (3-month SOFR), for each bank *b*, at the start of the projection horizon and uses this spread to model changes in these floating rate expenses over the forecast period.

$$Swap\ Spread_b = \frac{Swap\ Expense_b}{Notional\ Amount\ of\ Unhedged\ Notes_b} \times 4 - SOFR3Mo$$

Because the swap spread cannot be calculated at the security level, the same implied spread is applied to all swapped payments. To do so, the fixed and floating parts of the swap are calculated for each security:

$$Swap\ receipt_{i,t} = Coupon_{i,t} \times \%Swapped_{i,t} \times NotionalAmount_{i,t}$$

$$Swap\ payment_{i,t} = \left(SOFR3M_t + SwapSpread_b\right) \times \%Swapped_{i,t} \times NotionalAmount_{i,t}$$

$$Swap\ adjustment_{i,t} = \frac{Swap\ payment_{i,t} - Swap\ recepit_{i,t}}{4}$$

The Board assumes that swaps are fairly priced at origination. Hence, the benefit of a swap at origination will be offset by the cost of purchasing the hedge. As a consequence, the Board assumes that firms do not renew swaps once the underlying note has matured.

<!-- Source PDF page 158 -->

<a id="sec-138"></a>

##### (b) Assumptions and Limitations

In using the structural model to forecast subordinated debt expenses, the Board makes a number of assumptions, described as follows:

- debt maturing during the forecast period is replaced with subordinated debt instruments of the same structure and maturity, using scenario-consistent interest rates and credit

ratings;

- in the severely adverse scenario, firms’ credit ratings are downgraded by two notches (i.e., one letter grade). This assumption is motivated by Board historical analysis of
<!-- page 159 -->

downgrades of financial firms during the 2008 financial crisis and the policy statement

principles of conservatism;

- refinanced fixed-rate debt pays the scenario-consistent interest rates and maturity-matched corporate yield in the macroeconomic scenario. These yields are calculated

based on non-financial corporates and thus avoid incorporating historical data on bank

yield curves that might include too-big-to-fail or other discounts related to expected

government support of the financial system in a crisis; and

- firms with more floating-rate debt or more fixed-to-floating swaps will have more variation in interest expense than banks with fixed-rate debt.

During model performance exercises, the Board observed that the current structural model generally outperforms panel regression models in terms of forecasting performance. This difference can be largely explained by the dynamics of the subordinated debt model. The model accounts for whether a firm needs to roll over its existing subordinated debt in an environment when rates might change. It also accounts for variation in firms’ exposures to floating- and fixed-rate debt instruments, their interest-rate hedging capacities, and amortization.

As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle. The Board proposes a regression model for interest expense on other borrowing, which includes interest expense on subordinated debt together with interest expense on short-term borrowing and other interest-bearing liabilities.

<!-- Source PDF page 159 -->

<a id="sec-139"></a>

##### (c) Questions

*Question A134: The Board seeks comment on the alternative approach which considers interest expense on subordinated debt together with interest expense on short-term borrowing and other interest-bearing liabilities, as compared to the Board's current structural approach to project interest expenses on subordinated debt.*
<!-- page 160 -->

*Question A135: Is there any other alternative model that the Board should consider to project interest expenses on subordinated debt? What would be the advantages and disadvantages of using that alternative?*

*Question A136: Are there additional factors that the Board should consider in modeling interest expenses on subordinated debt? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A137: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of interest expenses on subordinated debt?*

*Question A138: Are there additional data sources the Board should consider incorporating in its modeling of interest expenses on subordinated debt? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 160 -->

<a id="sec-140"></a>

### n. Nonparametric Models

The Board currently uses a nonparametric approach to model the following components:

- all other noninterest income; and
- all other noninterest expense. The Board has observed that income or expense flows from these components tend to be highly volatile from quarter to quarter and often include non-recurring income or expense items. In addition, there is a high degree of heterogeneity across banks in the nature of expenses reported in these components.

While evaluating the possibility of modeling these components as panel regressions, and following the standard procedure for model specification, the Board did not find statistically
<!-- page 161 -->

significant and consistent relationships between the income or expenses flows of these components and macroeconomic variables in the scenario.

Moreover, by analyzing historical data, the Board did not find that income or expense flows of these components respond directly to short-term interest rates, concluding that these components are not good candidates to structural models.

Finally, the Board excludes noninterest expenses that are non-recurring in nature and arise as a result of mergers, acquisitions, or divestitures. The Board assumes that these expenses are of one-off nature and will not be incurred in the future.

<!-- Source PDF page 161 -->

<a id="sec-141"></a>

#### (1) All Other Noninterest Income

All other noninterest income is a residual component of noninterest income and includes deposit or lending related fee income, advisory or other asset-based fees, and commissions and fees on services. It represents a residual category that is not already modeled elsewhere in the other components discussed above. The Board computes this component as a residual of all noninterest income components:

$$\begin{aligned}&all\ other\ noninterest\ income \\ &= total\ noninterest\ income - (trading\ revenue \\ &\quad + noninterest\ income\ on\ service\ charges\ on\ deposits \\ &\quad + noninterest\ income\ from\ net\ servicing\ fees \\ &\quad + noninterest\ income\ on\ investment\ banking\ fees \\ &\quad + fiduciary\ income, insurance\ fees, and\ annuity\ fees)\end{aligned}$$

<!-- Source PDF page 161 -->

<a id="sec-142"></a>

##### (a) Model Description

Following common methods for other nonparametric models, the procedure to calculate the projections is the following:
<!-- page 162 -->

- reported all other noninterest income flow for every firm is divided by total assets balances[^57] to compute a ratio;
- the most recent eight quarters of historical data for the ratio (starting and including the lift-off year) is used to compute an 8-quarter median;
- the median is multiplied by the asset balances at the start of the projection horizon; and
- this value (median multiplied by balances) is used as a flat dollar projection for each firm for each quarter in the projection horizon, consistent with the flat balances assumption

held in stress testing.

The equivalent equation used to project the flow of all other noninterest income, for $F_{i,q}$, for each firm $i$ in every quarter $q$ on the projection horizon can be written as:

**Equation A29** – All Other Noninterest Income Projection

$$F_{i,q} = median\left(\frac{NII_{i,q0}}{assets_{i,q0}}, \frac{NII_{i,q0-1}}{assets_{i,q0-1}}, \frac{NII_{i,q0-2}}{assets_{i,q0-2}}, \frac{NII_{i,q0-3}}{assets_{i,q0-3}}, \frac{NII_{i,q0-4}}{assets_{i,q0-4}}, \frac{NII_{i,q0-5}}{assets_{i,q0-5}}, \frac{NII_{i,q0-6}}{assets_{i,q0-6}}, \frac{NII_{i,q0-7}}{assets_{i,q0-7}}\right) \times assets_{i,q0}$$

In this projection equation:

- $F_{i,q}$ is the projected flow (in dollars) of all other noninterest income for firm $i$ in quarter $q$ of the projection horizon;
- $NII_{i,q0}$ is the historical flow (in dollars) of all other noninterest income for firm $i$ in the lift-off quarter $q0$; and
- $assets_{i,q0}$ are the historical balances (in dollars) of total assets for firm $i$ in the lift-off quarter $q0$.

##### (a.) Assumptions and Limitations

The central assumption for the use of nonparametric models based on the recent firm-level median is that the revenue or expense component is not expected to vary based on macroeconomic conditions or economic distress. In practice, this approach assumes that the best possible forecast for the ratio is to use the median over recent history. The median is chosen, instead of the mean, to partially smooth out the high volatility observed in historical data. One limitation of the current nonparametric approach is that, for any additional scenario explored by the Board, projections under nonparametric models are going to be the same for every firm.
<!-- page 163 -->

When compared with the regression-based alternatives, the Board understands that the current modeling approach for all other noninterest income is as conceptually sound as regression-based alternatives and is consistent with the Policy Statement principles of simplicity and explainability.

An alternative approach is to model all other noninterest income utilizing information from firms’ projections. As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle, which is based on firms’ projections. The Board proposes a model of total noninterest income based on data reported in the FR Y-14A schedule and aggregate industry-level time series and discusses its assumptions and limitations. The proposed model of total noninterest income subsumes the current model of all other noninterest income, together with the current models for other components of noninterest income.

<!-- Source PDF page 163 -->

<a id="sec-143"></a>

##### (b) Questions

*Question A139: The Board seeks comment on the alternative approach based on firms’ projections reported in FR Y-14A, as compared to the Board's current approach to project all other noninterest income?*

*Question A140: Should the Board consider modeling all other noninterest income components at a more granular level? What would be the advantages and disadvantages of that choice?*

*Question A141: Is there any other alternative model that the Board should consider to project all other interest income? What would be the advantages and disadvantages of using that alternative?*

*Question A142: Are there additional factors that the Board should consider in modeling all other interest income? If so, what are they? What data source could the Board use to*
<!-- page 164 -->

*incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages of incorporating those additional factors?*

*Question A143: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of all other interest income?*

*Question A144: Are there additional data sources the Board should consider incorporating in its modeling of all other interest income? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 164 -->

<a id="sec-144"></a>

#### (2) All Other Noninterest Expense

All other noninterest expense is a residual component of noninterest expense components and contains a wide variety of expense items, primarily data processing and consulting and advertising expenses, as well as clearing fees, travel commissions, and other non-traditional banking business expenses. As reported, this line item also contains other real estate owned and operational risk expenses, which are excluded from the pre-provision net revenue model because they are modeled elsewhere in the stress test.[^58]

The Board computes this component as a residual of all noninterest expense components:

**Equation A30** – All Other Noninterest Expense

$$\begin{aligned}&all\ other\ noninterest\ expense \\ &= total\ noninterest\ expense\ except\ other\ real\ estate\ owned\ and\ operational\ risk\text{[^59]} \\ &- (noninterest\ expense\ on\ fixed\ assets\ + \ noninterest\ expense\ on\ compensation)\end{aligned}$$

<!-- page 165 -->

<!-- Source PDF page 165 -->

<a id="sec-145"></a>

##### (a) Model Description

The method used to calculate projections for all other noninterest expense follows the same approach as the method described above for noninterest income all other.

The nonparametric projection for computing all other noninterest expense is the following:

- reported all other noninterest expense flow for every firm is divided by total assets balances to compute a ratio (the Board may exclude non-recurring expenses, such as the

special assessment from the FDIC or non-recurring expenses arising from mergers,

acquisitions, or divestments);

- the most recent eight quarters of historical data for the ratio (starting and including the lift-off year) is used to compute an 8-quarter median;
- the median is multiplied by the asset balances at the start of the projection horizon; and
- this value (median multiplied by balances) is used as a flat dollar projection for each firm for each quarter in the projection horizon, consistent with the flat balances assumption

held in stress testing.

The equivalent equation used to project the flow of all other noninterest expense, for $F_{i,q}$, for each firm $i$ in every quarter $q$ on the projection horizon can be written as:

**Equation A31** – All Other Noninterest Expense Projection

$$F_{i,q} = median\left(\frac{NIE_{i,q0}}{assets_{i,q0}}, \frac{NIE_{i,q0-1}}{assets_{i,q0-1}}, \frac{NIE_{i,q0-2}}{assets_{i,q0-2}}, \frac{NIE_{i,q0-3}}{assets_{i,q0-3}}, \frac{NIE_{i,q0-4}}{assets_{i,q0-4}}, \frac{NIE_{i,q0-5}}{assets_{i,q0-5}}, \frac{NIE_{i,q0-6}}{assets_{i,q0-6}}, \frac{NIE_{i,q0-7}}{assets_{i,q0-7}}\right) \times assets_{i,q0}$$

In this projection equation:

- $F_{i,q}$ is the projected flow (in dollars) of all other noninterest expense for firm $i$ in quarter $q$ of the projection horizon;
- $NIE_{i,q0}$ is the historical flow (in dollars) of all other noninterest expense for firm $i$ in the lift-off quarter $q0$; and
- $assets_{i,q0}$ are the historical balances (in dollars) of total assets for firm $i$ in the lift-off quarter $q0$.

<!-- Source PDF page 165 -->

<a id="sec-146"></a>

##### (b) Assumptions and Limitations

Regarding nonparametric models, the central assumption for the use of the recent firm-level median is that the expense component is not expected to vary based on macroeconomic
<!-- page 166 -->

conditions or economic distress. In the case of this component, the Board is assuming this behavior for all other expenses. A limitation of the flat median approach is that, for any additional scenario explored by the Board, projections under nonparametric models are going to be the same for every firm.

When compared with the regression-based alternatives, the Board understands that the current modeling approach for all other noninterest expense is as conceptually sound as regression-based alternatives and is consistent with the Policy Statement principles of simplicity and explainability.

As discussed in Section A.v., the Board is proposing an alternative to the current model for the 2026 stress test cycle. The Board proposes a model based on projecting a firm’s aggregate noninterest expense as a function of projected revenues (net interest income plus noninterest income) and the firm’s projected efficiency ratio.[^60] This alternative avoids the projection of components of noninterest expense separately, such as all other noninterest expense.

<!-- Source PDF page 166 -->

<a id="sec-147"></a>

##### (c) Questions

*Question A145: The Board seeks comment on the alternative approach based on firm’s projected efficiency ratio, as compared to the Board's current approach to project all other noninterest expense.*
<!-- page 167 -->

*Question A146: Is there any other alternative model that the Board should consider to project all other interest expense? What would be the advantages and disadvantages of using that alternative?*

*Question A147: Are there additional factors that the Board should consider in modeling all other interest expense? If so, what are they? What data source could the Board use to incorporate those additional factors, and how could they be incorporated into the model? What would be the advantages and disadvantages?*

*Question A148: Are there additional data items reported on the FR Y-9C, FR Y-14, or other relevant forms that the Board should consider incorporating in its modeling of all other noninterest expense?*

*Question A149: Are there components of noninterest expense currently reported as part of all other noninterest expense that might exhibit macrosensitivity? If so, what are these components? Are there additional models that the Board should consider for these components of all other noninterest expense? What would be the advantages and disadvantages in modeling these components separately?*

*Question A150: Are there additional data sources the Board should consider incorporating in its modeling of all other noninterest expense? If so, which ones? What would be the advantages and disadvantages of adding these data sources?*

<!-- Source PDF page 167 -->

<a id="sec-148"></a>

## v. Proposed Models for 2026 Pre-Provision Net Revenue Components

The Board is proposing to use a new suite of models for all components of pre-provision net revenue in the 2026 stress test cycle. These proposed models would depart from the panel regression-based approach currently used for most pre-provision net revenue components. The
<!-- page 168 -->

proposed models aim to better capture firms’ business practices by using granular position data to model net interest income and bank projections to model noninterest income and expense. The Board is soliciting public input on these proposed models.

The current regression models are subject to certain limitations stemming from the autoregressive term that is needed for many components to capture variation over time and across firms in portfolio composition. In particular, the autoregressive term introduces a dependence on lagged performance. This contributes to volatility in projections that runs counter to the Policy Statement principles of robustness and stability. Together with the various fixed effects and seasonality indicators, the regression models may also produce results that are challenging to interpret. As such, the Board has prioritized the Policy Statement principles of stability, simplicity, and transparency in constructing and considering alternative models.

The Board is proposing four different model types for the components of pre-provision net revenue for the 2026 stress test. The model types are (1) structural models, (2) regression models, (3) discount factor models, and (4) efficiency ratio models. Table A6 presents the proposed model type for each of the 23 pre-provision net revenue components.

**Table A6** – Pre-Provision Net Revenue Components Specification Summary: Proposed Model Types for 2026|

| PPNR Component | Model Type |
|---|---|
| **Structural models for interest income** | |
| Loans | Structural |
| Deposits with banks and other | Structural |
| U.S. Treasuries | Structural |
| Mortgage-backed securities | Structural |
| Other securities | Structural |
| Other interest/dividend-bearing assets | Structural |
| **Structural models for interest expense** | |
| Domestic time deposits | Structural |
| Other domestic deposits | Structural |
| Foreign deposits | Structural |
| Federal funds purchased and securities sold under agreements to repurchase | Structural |
| **Regression models** | |
| Net interest income on trading assets and liabilities | Regression |
| Interest expense on other borrowing | Regression |
| **Noninterest income discount factor models** | |
| Deposit-related | Discount factor |
| Credit and charge card loan-related | Discount factor |
| Other loan-related | Discount factor |
| Sales and trading | Discount factor |
| Investment banking and merchant banking/private equity | Discount factor |
| Asset management | Discount factor |
| Wealth management | Discount factor |
| Investment services | Discount factor |
| Treasury services | Discount factor |
| Miscellaneous | Discount factor |
| **Efficiency ratio model** | |
| Noninterest expense | Efficiency ratio |

<!-- page 169 -->

For net interest components, the proposed models generally use granular data on maturities and interest rate characteristics of assets and liabilities to project future revenues or expenses. These granular structural models tie projections more closely to banks’ actual assets and liabilities at the beginning of the projection horizon. These models rely on known characteristics of bank positions and therefore are conceptually simple and transparent. For certain net interest components, granular data are not available. For these components, the proposed models consist of structural models in the form of calculators or simple panel regressions that tie interest income earned on the relevant assets and liabilities to a
<!-- page 170 -->

contemporaneous reference interest rate. While these approaches are not as precise as the granular models, they are simple, stable, and transparent by construction.

For noninterest income and expense components of pre-provision net revenue, the proposed models also represent a departure from the current regression model framework built on historical data from the FR Y-9C. These proposed models for both noninterest income and noninterest expense rely on firm projections under the supervisory severely adverse scenario from the FR Y-14A. While these two sets of components are modeled using FR Y-14A data, they are motivated by different considerations.

Similar to net interest income components, a bank’s noninterest income depends on specific aspects of its business practices. However, the Board has not collected historical data of sufficient granularity to precisely represent these practices, nor has it identified simple structural models capable of accounting for different practices across banks. As such, the Board has focused the construction of the proposed noninterest income models on two considerations. First, absent the ability to precisely capture the details of banks’ business practices, the approach should be simple. Second, given challenges in modeling these business practices via the available historical data, industry projections of noninterest income under stress are an effective way to capture and reflect knowledge of the relevant business practices.

The proposed approach models ten distinct components of noninterest income at the industry level. For each component, aggregate bank projections from the FR Y-14A schedules are used to produce a path of noninterest income over the projection horizon. Firm-level supervisory projections are then obtained by weighing the component-level projections according to a given bank’s recent mix of revenues across these components.
<!-- page 171 -->

In the proposed model for noninterest expense, the Board leverages long-term relationships that exist between a bank’s income and expense streams. This approach contrasts with the 2025 suite of pre-provision net revenue models, in which expenses evolve independently of income. The link between expenses and income is in some cases structural, such as for certain components of compensation expenses. For noninterest expenses more broadly, analysis of banks’ historical data as well as of their projections submitted via the FR Y-14A suggests a stable relationship with net interest income and noninterest income over time.

The proposed model leverages this relationship via the efficiency ratio, a commonly used financial metric that is defined as the ratio of noninterest expense to the sum of net interest and noninterest income. The proposed model rests on the observation that after controlling for variation in the mix of business activities, banks tend to predict an expense ratio path under stress that is stable across firms and over different stress testing cycles. The efficiency ratio path is estimated via an industry model of firm projections from previous stress testing exercises. This industry model is then used to project a given bank’s noninterest expense using income projections from the other alternative supervisory models and the bank’s revenue mix in the period before the start of the projection horizon. This modeling approach is simple and transparent. It also reflects the business practice of managing net revenues in total, in addition to managing individual revenue and expense components. Therefore, this approach supports the principle of stability, as the efficiency ratio-based expense projections will by construction rise and fall with the projected income.

In constructing the proposed models for noninterest income and noninterest expense, the Board weighed the tradeoff between the Policy Statement principle of independence and those of transparency, simplicity, and stability. In particular, basing these proposed models on firm-
<!-- page 172 -->

provided inputs represents a certain departure from the principle of independence. However, the Board believes that the potential gains seen with respect to other principles outweigh any losses with respect to the independence principle. Furthermore, the Board intends to monitor the firm projections, and the internal models that generate those projections, to ensure that the projections remain robust and informative over time given their heightened importance in the proposed models. The Board seeks comment on whether an appropriate tradeoff has been achieved between the above principles.

The proposed models are described in detail below.

<!-- Source PDF page 172 -->

<a id="sec-149"></a>

### a. Proposed Structural Models

The Board is proposing using structural models for 10 interest income and expense components in the 2026 stress test. They are:

- interest income on loans;
- interest income on deposits with banks and other;
- interest income on U.S. Treasuries;
- interest income on mortgage-backed securities;
- interest income on other securities;
- interest income on other interest/dividend-bearing assets;
- interest expense on domestic time deposits;
- interest expense on other domestic deposits;
- interest expense on foreign deposits; and
- interest expense from federal funds purchased and securities sold under agreements to repurchase.

The structural models being proposed for the above components are based on granular data reported in FR Y-14Q, Schedule G; FR Y-14Q, Schedule B; FR Y-14Q, Schedule M; and FR Y-14M. Details regarding how each component is modeled are described below.

Advantages of the proposed structural models when compared to the regression models are enhanced clarity and explainability. Structural models also avoid statistical estimation,
<!-- page 173 -->

making variability of projections over stress testing cycles fully explainable by balances reported for each bank and the variation in the interest rate scenario paths.

<!-- Source PDF page 173 -->

<a id="sec-150"></a>

#### (1) Interest Income on Loans

<!-- Source PDF page 173 -->

<a id="sec-151"></a>

##### (a) Model Description

Similar to several other pre-provision net revenue components, interest income on loans is currently modeled using a panel regression model with an autoregressive term. The Board proposes an alternative set of models for interest income on loans. In contrast to the regression models, the proposed loan interest income model is developed using a granular, bottom-up approach with data from the FR Y-14M and FR Y-14Q regulatory reports. This granular approach provides the ability to derive changes in interest income in the projected scenario directly from loan characteristics, specifically the type of interest rate variability. There are multiple benefits to using this bottom-up approach rather than the regression models. This bottom-up approach is closer to the business-as-usual calculations performed by institutions for accounting and forecasting purposes. This approach would more accurately reflect the income impact of loan characteristics within a scenario and would therefore enable easier interpretation of results. This approach also results in a model with the appropriate sensitivity to projected scenarios.

The proposed loan interest income model projects 9 quarters of interest income using the following specification:

**Equation A32** – Interest Income on Loans Projection

$$Loan\ interest\ income_{b,p,i,t} = Loan\ balance_{b,p,i,t} * Interest\ income\ rate_{b,p,i,t}$$

*where:*

- *b = firm;*
<!-- page 174 -->

- *p = product;*
- *i = segment;* and
- *t = projection quarter*|

$Loan\ balance_{b,p,i,t}$ is calculated by taking the percentage of outstanding balance for segment $i$ by firm $b$ and product $p$ and then multiplying it by the portfolio balance from FR Y-14 Schedules. Loan balances are held constant throughout the 9 projection quarters for all loan portfolios, consistent with the constant balance assumption for the stress test exercise. Any reduction in exposure arising from default, prepayment, or amortization will be replenished by newly originated loans within the same projection quarter, such that the portfolio balance remains unchanged. Adding newly originated loans in this manner is similar to loan re-origination done for the credit loss projections across the loan portfolio.

$Interest\ income\ rate_{b,p,i,t}$ represents the interest rate in quarter $t$ for firm $b$, product $p$, and segment $i$. Interest rate characteristics from FR Y-14 reports are used to determine the interest rate sensitivity in the projected scenario. The proposed loan interest income model does not estimate any components but simply calculates interest rates from the scenario, loan information, and estimated loss rates from the Retail and Wholesale models. The interest rate reset indices provide a direct link between the scenario and the projected interest rates.

<!-- Source PDF page 174 -->

<a id="sec-152"></a>

##### (b) Portfolio Segmentation

The proposed loan interest income model utilizes segments within portfolios primarily to reflect new origination’s interest income characteristics. For each segment, an average jump-off interest rate weighted by outstanding balance is used as the starting point for projecting the segment level interest rate. A segment with a weighted average of these jump-off interest rates captures differences in interest income across banks and portfolios. Differences in loan
<!-- page 175 -->

characteristics within a segment, such as risk profile, appear as differences in the weighted average. The primary determinant of the segmentation scheme is interest rate sensitivity. The key considerations to segment a portfolio’s interest income is rate type: each retail or wholesale portfolio is segmented into fixed-rate and variable-rate exposures. This is a critical segmentation step to separately account for when interest rates change during the projection.

<!-- Source PDF page 175 -->

<a id="sec-153"></a>

###### Wholesale

Wholesale interest income projections are organized into two parts: Corporate and Commercial Real Estate (CRE). Data used in the segmentation of wholesale balances are sourced from FR.[^61] Each section is segmented by asset classification: held for investment (HFI) and fair value option/held for sale (FVO/HFS).

<!-- Source PDF page 175 -->

<a id="sec-154"></a>

###### Corporate

The corporate section of loan level interest income is segmented by 11 disclosure categories and loan types (referenced as a portfolio). Portfolios included in the corporate section are: (1) commercial and industrial loans, (2) domestic owner-occupied CRE loans, (3) other non-consumer loans, (4) other leases, (5) loans to foreign governments, (6) international owner-occupied CRE loans, (7) agricultural loans, (8) loans to financial institutions, (9) loans for purchasing and carrying securities, (10) domestic farmland loans, and (11) international farmland loans. Most of the firm’s corporate portfolios (16 out of 22) are further segmented by the interest rate variability since this provides a clear distinction on when the interest rate will be adjusted. The two broad types of interest rate variability, fixed-rate and variable-rate,[^62] are used to
<!-- page 176 -->

segment each portfolio. The interest income model treats mixed-rate and demand loans (loans where the lender can demand full repayment at any time) as variable-rate. Fee-only loans are assumed to generate no interest income. Hence, they are not used to calculate the average interest rate, and their outstanding balance percentages are excluded from the total balances calculation.

Loans for purchasing and carrying securities, domestic farmland loans, and international farmland loans are not segmented by interest rate variability because they have no loan-level data on the FR Y-14Q H.1 schedule. This limits further segmentation and requires additional assumptions to model interest income for these portfolios. The Board assumes, for these portfolios, the same bank-level interest rate spread as reported in their variable-rate lending to depository institutions. This assumption is based on loan-level data on non-purpose margin loans (NPML), which have similar characteristics to loans for purchasing and carrying securities. Currently, the FR Y-14Q Schedule H.1 schedule is able to identify NPMLs. The majority of NPMLs were variable-rate, so the Board assumes loans for purchasing and carrying securities have variable rates.

<!-- Source PDF page 176 -->

<a id="sec-155"></a>

###### CRE

The CRE section of loan-level interest income is first segmented into six disclosure loan types (also referred to as portfolios) as defined in FR Y-9C: (1) domestic construction loans, (2) domestic multifamily loans, (3) domestic non-owner occupied commercial real estate loans, (4) international construction loans, (5) international multifamily loans, and (6) international non-owner occupied commercial real estate loans. CRE segmentation is similar to Corporate segmentation where interest rate variability splits the portfolio by fixed-rate and variable-rate
<!-- page 177 -->

interest rates. With the asset classification segmentation, the total number of CRE segments is 24.

<!-- Source PDF page 177 -->

<a id="sec-156"></a>

###### Retail

Retail interest income projections are organized into four sections: (1) Mortgage (including first lien, home equity loans, and home equity lines of credit), (2) auto loan, (3) consumer credit card, and (4) other non-core credit products such as small business loans, SME cards, private student loans, and consumer finance products. Segmentation within a retail portfolio is driven by the rate structure (i.e., fixed vs. variable rate), product type, and credit risk. Data used in the segmentation of retail products are sourced from regulatory reports including FR Y-14M and FR Y-14Q schedules and include both loan-level and segment-level attributes. Data limitations prevent further segmentation of the non-core products.

<!-- Source PDF page 177 -->

<a id="sec-157"></a>

###### Mortgage

The segmentation of mortgage and home equity products is driven primarily by asset classification, loan rate, and loan structure. They are segmented first by asset classification (HFI and FVO/HFS) and then rate structure (i.e., fixed-rate mortgage vs. adjustable-rate mortgage [ARM]). Additional segmentation variables, such as loan term (30-year vs. 15-year) and origination risk segments (FICO ≥ 720 vs. FICO < 720), were considered, but ultimately not adopted due to their immaterial impact on projected interest income. Balance-weighted average loan rates are calculated by segment and by firm based on the FR Y-14M loan-level data and used as inputs in interest income projections.
<!-- page 178 -->

<!-- Source PDF page 178 -->

<a id="sec-158"></a>

###### Auto Loan

Auto loans are reported in the FR Y-14Q schedule A.2 at the segment level. Auto loans are typically fixed-rate products, so the Board assumes that the portfolio is comprised of auto loans with fixed interest rates. The Board treats immaterial HFS auto loan balances reported in FR Y-9C as HFI loans at the firm level.

The portfolio is segmented into new vehicle loans and used vehicle loans, driven primarily by the differences in rates between these two categories. The Board calculates balance-weighted average interest rates by segment and by firm and uses them as inputs for interest income projection. Trends in balance-weighted average interest rates were analyzed by product (i.e., new-vehicle vs. used-vehicle loans) and compared against the Prime Rate to determine the spread for the new origination rate. The Board also reviewed FR Y-14Q defined origination risk segments but ultimately does not propose to adopt these due to their immaterial incremental impact on the projected interest income.

<!-- Source PDF page 178 -->

<a id="sec-159"></a>

###### Consumer and Small Business Credit Card

Consumer credit cards are segmented into two product types: consumer bank cards, where consumers can carry a balance; and consumer charge cards, which are historically expected to be paid off by the due date, but recent charge card products allow minimum payment with accrued interest income, which are reflected in the alternative model. Most credit cards have variable rates and approximately 10 percent have short-term fixed rates. Since the short-term rates change in the scenario, the Board assumes that all credit card balances have variable rates.
<!-- page 179 -->

Credit card interest income depends on both the portion of balance that revolves and the interest rate. The key modeling challenge lies in estimating the percentage of balances that revolve and bear interest charges. Balances paid in full prior to the due date do not incur interest charges and therefore do not contribute to interest income. The Board utilizes the following approach to identify revolving credit card accounts. An account is primarily classified as a revolver if it has been active in the last 12 months and has had at least one positive finance charge in any of the last 3 months. This classification is used to estimate the percentage of balances revolving and therefore earning interest income.

Currently all firms use the Prime Rate as the benchmark index to set credit card APR, and both the interest rate and interest spread are reported in FR Y-14M. The balance-weighted interest rate, interest spread, and the Prime rate are used to determine a constant projected spread at the segment level. The prime rate from the scenario is utilized as the benchmark variable rate. Balance-weighted average interest rate, interest spread, and percentage of balance revolving are calculated by segment and firm and used as inputs in credit card interest income projection.

The Board proposes modeling small business cards separately but following a similar structure. Small business cards are also assumed to carry variable rates, with interest income driven by the interest rate and the portion of balances that revolve. The transactor-revolver methodology applied to consumer cards is similarly used to estimate the revolving balance share for small business cards. Segment-level data from FR Y-14M, including interest rate and spreads, support the projection assumptions.

<!-- Source PDF page 179 -->

<a id="sec-160"></a>

###### Other Consumer Products

The other consumer portfolio is a heterogenous category that includes multiple consumer credit products for which interest rate is not reported in the FR Y-14Q retail schedule regulatory
<!-- page 180 -->

filing. This category includes, but is not limited to, private student loans, other consumer loans, international auto loans, international mortgage, international home equity, international small business loans, non-purpose lending, and other miscellaneous consumer finance products.

Due to the lack of interest rate data, no segmentation is applied to these credit products. Instead, jump-off interest rates are assigned at the aggregate product-type level, using the firm-level earned interest rates reported in the FR Y-14Q pre-provision net revenue line-item report for the most closely aligned business line. Jump-off spread is derived as the difference between jump-off interest rate and Prime Rate and is held constant over projection quarters. This approach ensures consistency while maintaining a conservative and supportable basis for interest income projections.

<!-- Source PDF page 180 -->

<a id="sec-161"></a>

###### Projected Interest Income Rate

Interest income consists of interest income from existing portfolios and from new originations during the projection periods under the flat balance assumption. Both wholesale and retail portfolios re-originate based on different runoff rate at each projection quarter. The Board proposes to model the interest rate path differently for fixed-rate and variable-rate products over the projection window. All portfolios have a portfolio-specific interest rate floor that will bind if the projected interest rate decreases to the stated floor.

<!-- Source PDF page 180 -->

<a id="sec-162"></a>

###### Variable-rate products

For variable-rate products, projected interest rates are determined using the base rate-related variables from the scenario file (discussed below), combined with an estimated spread. Most variable rates reset quarterly while balances of variable-rate products remain unchanged under the flat balance assumption. The projected interest rate is calculated as:
<!-- page 181 -->

**Equation A33** – Variable-Rate Products Interest Rate Projection

$$IR_{(b,p,i,t)} = BaseRate_{(p,i,t)} + Spread_{(b,p,i,t=0)}$$

*where:*

- $IR_{(b,p,i,t)}$ represents interest rate for firm $b$, product $p$, and segment $i$ at time $t$;
- $BaseRate_{(p,i,t)}$ represents the scenario base rate at quarter *t for product p*; and
- $Spread_{(b,p,i,t=0)}$ represents the initial spread for firm $b$, product $p$, and segment $i$ which is held constant over time.

<!-- Source PDF page 181 -->

<a id="sec-163"></a>

###### Base rate assumptions

The base rate determines the magnitude of interest rate change in the scenario. For retail variable-rate products, including consumer and small business credit cards and home equity line of credit, the Board proposes to use the Prime Rate as the base rate. Adjustable-rate mortgage products directly use mortgage rate as the base rate. For wholesale, the Board proposes to use the three-month Treasury yield as the base rate. The majority of balances in wholesale are variable-rate, thus the projected base rate is most responsible for changes in the projected interest income.

<!-- Source PDF page 181 -->

<a id="sec-164"></a>

###### Spread Estimation

The spread is defined as the difference between the balance-weighted average interest rate and the base rate, and it varies by firm, product, and segment. The level of granularity for spread estimation depends on the product segment and data availability. When data is limited, the Board proposes to determine spreads through other alternative data sources, especially for the non-core portfolio where the Board uses expert judgment to split it into variable rate and fixed-rate products.

Given that the stress test assumes constant balances, and the fact that the interest rate spread will not get updated during the projection horizon, the Board proposes replacing variable
<!-- page 182 -->

rate facilities that default, mature, or run-off with the same loan type. This allows the interest income equation above to calculate the interest rate at time *t*. Changes in the interest rate for variable-rate balances are completely determined by changes in the scenario variable.

<!-- Source PDF page 182 -->

<a id="sec-165"></a>

###### Fixed-Rate Products

For the fixed-rate products, the Board proposes to use the balance-weighted origination rate by firm, product, and segment at jump-off, and the rates are assumed to remain unchanged throughout the stress test projection horizon except if they terminate.

**Equation A34** – Fixed-Rate Products Interest Rate Projection

$$IR_{(existing,t)} = IR_{(existing,t=0)}$$

For new originations, origination interest rates are projected using a modification to the fixed-rate product interest rate equation:

**Equation A35** – Origination Interest Rates Projection

$$IR_{(p,i,t,\ new\ orig)} = BaseRate_{(p,i,t)} + Spread_{(p,i,t=0)}$$

The spread for fixed-rate balances is calculated differently than variable-rate balances. For retail, instead of using the average rate of all loans, only new origination loans are used.

**Equation A36** – Spread for Fixed-Rate Projection

$$Spread_{(p,i,t=0)} = weighted\ avg\ IIR\ for\ new\ originations_{(p,i,t=0)} - Base\ rate_{(p,i,t=0)}$$

For wholesale, the spread is calculated from the average rate of all loans at the jump-off quarter and the base rate from the median origination date ( *t* - *a*) for that portfolio. The base rate applied is the same as the base rate for floating: the Prime Rate for retail and the three-month Treasury yield for wholesale.

**Equation A37** – Spread for Wholesale Projection

$$Spread_{(b,p,i,t=0)} = balance_{weighted}\,avg\ IIR_{(b,p,i,t=0)} - Base\ rate_{(t-a)}$$

<!-- page 183 -->

The reason for this difference is that fixed interest rates were set at some point in the past. Two fixed-rate loans with the same risk profile but set during different interest rate environments will likely have different interest rates. Using the jump-off scenario variable will likely result in a biased calculation of the interest rate spread. Using only new originations minimizes this bias but limits the number of loans used in the calculation. This minimizes the bias because all fixed-rate loans are set during the same interest rate environment. However, this assumes similar risk profiles for loans originating at the jump-off and in the previous quarter. Using the median origination date may better account for changing risk profiles but come at the expense of likely measurement error.

The projected fixed-rate interest rate is a weighted average of the existing interest rate, which is not updated, and the new origination rate calculated from the spread and base rate. Both interest rates are combined to calculate the fixed interest rate for that portfolio.

**Equation A38** – Projected Fixed-Rate Interest Rate

$$IR_{existing,(p,i,t)} = \left(1 - wt_{(p,i,t)}\right) * IR_{(existing,(p,i,t-1))} + wt_{(p,i,t)} * IR_{(new,p,i,t)}$$

The weight, $wt_{(p,i,t)}$, is the fraction of the portfolio that needs to be re-originated. This is derived from the default rate, prepayment rate, and maturity rate. Fixed-rate retail products include fixed-rate mortgage and home loans, auto loans, and most non-core loans. In wholesale, fixed-rate products are more common for CRE income-producing loans. Fixed-rate products are less sensitive to changes in the base rate because only a fraction of the portfolio gets updated interest rates.

<!-- Source PDF page 183 -->

<a id="sec-166"></a>

###### Industry Scalar

The Board calculates the interest income from different loan portfolios utilizing the methodology described above, which has several assumptions that are necessary primarily to
<!-- page 184 -->

address data limitations. The Board evaluates and adjusts for these data limitations by utilizing aggregated information from other reporting forms. Specifically, firms report interest income from each loan category in regulatory forms as well as financial statements. The Board proposes to “true-up” the calculations to the reported values using a multiplicative scalar by industry for each loan category.[^63] For example, if the calculated interest income in the domestic CRE portfolio is 95% of the value reported in the FR Y-14Q, Schedule G2, then the Board proposes to use a scalar of 1/0.95 = 1.05 to adjust the calculated value. This constant scalar is used to multiply the calculated domestic CRE interest income in each quarter in the projection horizon and this true-up adjustment minimizes the potential impact of data limitations on the projections.

<!-- Source PDF page 184 -->

<a id="sec-167"></a>

##### (c) Model Assumptions and Limitations

This proposed model is comprehensive and covers all the retail and wholesale products covered in the stress test. Consistent with the principle of simplicity in the Policy Statement, the model incorporates the following assumptions and acknowledges certain limitations:

<!-- Source PDF page 184 -->

<a id="sec-168"></a>

###### Assumptions

(1) The model assumes a flat balance over the projection horizon, meaning that portfolio

balances are held constant over time. The projected balance is the sum of remaining

balances of the existing portfolio and the new originations which are due to prepay,

maturity, and defaults.

(2) The model assumes that delinquent loans generate interest income. The impact of this

assumption is tested and immaterial.

(3) Interest income is quarterly compounded.

(4) Interest spreads are assumed to be constant over projection quarters.

(5) Most variable rates are repriced quarterly, aligning with changes in the projected base

rate.

(6) Balance-weighted segment-level fixed interest rates are assumed to remain unchanged

throughout the projection window, except for new originations.

(7) To reduce complexity, the model groups various products with similar rate structures and

applies consistent base rate and spread assumptions across products.
<!-- page 185 -->

<!-- Source PDF page 185 -->

<a id="sec-169"></a>

###### Limitations

Data availability imposes limitations on model accuracy and requires several assumptions for the interest income calculation. Differences in reporting instructions make comparisons between the model’s jump-off interest income calculations and reported FR Y-9C and FR Y-14Q, G.2 schedule interest income difficult. Scaling the model’s jump-off interest income to the reported interest income in the FR Y-14Q, G.2 schedule using the scalar brings these two numbers closer together.

<!-- Source PDF page 185 -->

<a id="sec-170"></a>

###### Retail Portfolio

The model assumes that all retail products (except for mortgages) use Prime Rate as base rate and constant spread by product, segment, and firm in projecting variable-rate and new origination rates. This assumption is to simplify the model structure and minimize firm and product variances.

Interest income projections for some retail products are limited by data availability and require assumptions on interest rate for each portfolio. There is no interest rate information for most non-core retails products including student loans, consumer finance products, international related loan products, and non-purpose loans. Auto loans are reported at the segment level with limited interest information. It also limits the accuracy of auto-loan interest income estimation.

<!-- Source PDF page 185 -->

<a id="sec-171"></a>

###### Wholesale Portfolio

The scenario-provided three-month Treasury yield is a strong proxy for the index values applied when interest rates are adjusted. More accuracy could be gained projecting interest income at the loan level instead of cutting the portfolio into segments. For fixed-rate loans, a more precise measure of when the jump-off interest rate was set could be used during the interest
<!-- page 186 -->

rate spread calculation. Also, for fixed-rate loans, using actual maturity dates and facility-specific probabilities of default would increase precision of when to update the interest rate. For variable-rate loans, a more granular approach would improve the accuracy of the interest rate floor. The model assumes a constant roll-off rate. This implies that extensions and prepayment and amortizations are not endogenous. It seems reasonable that an obligor is more likely to pay back a loan or seek an extension with different terms when interest rates are falling. Prepayment penalties and the lender needing to agree to the extension may limit to some extent the increased roll-off during a decreasing interest rate environment. Also, spreads will increase during stress which would further mitigate an endogenous roll-off rate. The model further accounts for this by applying a conservative roll-off rate for fixed-rate loans.

The model assumes that non-purpose margin loans (NPML) are a good proxy for loans for purchasing and carrying securities, domestic farm loans, and international farm loans. The Board used the loan-level analysis with only NPML as guidance to how to treat these missing portfolios.

The model does not increase draws from revolvers throughout the projection. This is different than credit loss models where there is an expected increase in draws from revolvers through exposure at default estimation. The expected change in interest income from increases in draw from revolvers during stress is minimal. Increases in draw from healthy firms will be short-lived precautionary liquidity insurance with firms paying them down quickly, while draws by firms that end up in bankruptcy are not expected to earn material interest income.

<!-- Source PDF page 186 -->

<a id="sec-172"></a>

##### (d) Questions

The Board is requesting public input on this proposed model for interest income on loans, including, but not limited to, input on the following questions:
<!-- page 187 -->

*Question A151: The Board seeks comment on the proposed approach to model interest income on loans, as compared to the Board's current panel regression model.*

*Question A152: Should the SOFR one-month maturity and the Prime Rate be used as the base rate for wholesale instead of the three-month Treasury Yield? Is there a scenario variable that would more accurately project changes in variable-rate interest rates? What would be the advantages and disadvantages of using these rates?*

*Question A153: Should corporate and CRE variable-rate balances be further segmented to vary the interest rate floor? The interest rate floor will bind if the projected scenario variable decreases the projected interest rate below the stated floor. Increases in segmentation will increase the accuracy of the interest rates by limiting interest rate movements when a floor should be binding.*

*Question A154: More generally, please provide comments on the segmentation described above for both wholesale and retail portfolios in the context of the calculation of interest income on loans.*

*Question A155: Should wholesale fixed-rated balances use the same approach as retail (i.e., only using new originations), for calculation of the interest rate spread? The current approach of wholesale fixed-rated balances is to use the base variable at the median origination date.*

*Question A156: A specific approach to assess whether a particular account is a revolver is outlined above. Is there a better approach to determining whether a particular account is a revolver? For example, an account could be classified as revolver if the account has finance charges observed on FR Y-14M reports.*
<!-- page 188 -->

*Question A157: The model uses a scalar to true-up at the jump-off quarter to account for data knowledge gaps and utilize the same scalar throughout the projection horizon. Is the use of the scalar reasonable? The scalar could be applied at the bank industry-wide level or at a portfolio level. Is one approach preferable to the other for any specific reason? Are there better approaches to address these data and knowledge gaps?*

*Question A158: Are there additional factors that the Board should consider to model changes to the interest rate spread?*

*Question A159: Interest rate risk hedges on loans have not been directly incorporated into the calculations described above, primarily due to data limitations. The Board is proposing additional data collection through an updated FR Y-14Q, Schedule B.2 to incorporate interest rate risk hedges for interest income on loans. Are there any special considerations that the Board should be aware of when considering how to account for interest rate risk hedges for interest income on loans?*

*Question A160: Are there additional factors that the Board should consider in modeling loan interest income?*

<!-- Source PDF page 188 -->

<a id="sec-173"></a>

#### (2) Interest Income on Deposits with Banks and Other

The Board proposes an alternative structural approach to model interest income on interest-bearing balances. Interest income from interest-bearing balances consists of interest-bearing deposits, including deposits held at the Federal Reserve and other institutions such as the Federal Home Loan Banks. The relevant balances are reported in line item 14 of the net interest income worksheet of FR Y-14Q, Schedule G. These balances have short durations, typically less than a single quarter, and the rate earned is usually directly linked to short-term interest rates.
<!-- page 189 -->

<!-- Source PDF page 189 -->

<a id="sec-174"></a>

##### (a) Model Description

Under this structural approach, interest income for this component at each quarter of the projection is calculated starting from a simple and intuitive assumption: interest-bearing balances earn a rate that responds directly to the short-term interest rate, as this is consistently observed in historical data. In particular, the Board assumes that the rate on this component is the 3-month U.S. Treasury rate.

More formally, let *Bb* be the total balance on interest-bearing balances and *Fb* be the interest income earned on this component. Then, for each firm *b* and for every period *t*

**Equation A39** – Interest Income on Deposits with Banks and Other

$$F_{b,t} = B_{b,t}Treasury3m_t$$

*where:*

- $Treasury3m$ is the 3-month Treasury yield.

Using this equation for the projection period, the projected flow of income $F_{b,q}$, for firm $b$ in quarter $q$ on the projection horizon, thus, can be calculated as:

$$F_{b,q} = B_{b,q}Treasury3m_q$$

The stress test assumes constant balances for all firms; therefore, $B_{b,q} = B_{b,q0}$ for all periods, where $B_{b,q0}$ represents the balances for the firm $b$ at lift-off quarter $q0$. This means that the projected flow of income is calculated based on the balances at the last quarter before the start of the projection.

<!-- Source PDF page 189 -->

<a id="sec-175"></a>

##### (b) Assumptions and Limitations

When using the structural model to model interest income on interest-bearing balances, the Board assumes that the rate each firm earns over the projection horizon is given by the 3-month U.S. Treasury rate. While the rate that the Federal Reserve pays on reserves tracks the 3-
<!-- page 190 -->

month U.S. Treasury rate closely, some fluctuations may be observed. Additionally, the rates paid by other depository institutions may be higher or lower.

<!-- Source PDF page 190 -->

<a id="sec-176"></a>

##### (c) Questions

The Board is requesting public input on this proposed model for interest income on loans, including, but not limited to, input on the following questions:

*Question A161: The Board seeks comment on the proposed approach to model interest income on interest-bearing balances, as compared to the Board's current panel regression model.*

*Question A162: Are there additional factors that the Board should consider in modeling interest income on interest-bearing balances? What data sources could the Board use to incorporate these additional factors?*

<!-- Source PDF page 190 -->

<a id="sec-177"></a>

#### (3) Interest Income on U.S. Treasuries

The Board proposes an alternative structural approach to model interest income on U.S. Treasuries and U.S. Government agency obligations (excluding mortgage-backed securities) that is based on security-level microdata available in form FR Y-14Q, Schedule B.

The approach relies on calculating interest income based on the sum of (a) coupon accruals for securities, (b) the amortization/accretion of amortized cost, and (c) the income impacts from any qualifying accounting hedges associated with the security. To calculate these items, the Board uses bond-specific details from FR Y-14Q, Schedule B.1 along with vendor data, including coupon rate and maturity. The Board makes certain simplifying assumptions or adjustments due to lack of information regarding either the security or hedging instrument in question.
<!-- page 191 -->

There are multiple benefits to using the structural, calculation-based approach rather than the regression models currently adopted to calculate stress test projections. While simplistic, this structural approach is closer to the business-as-usual calculations performed by institutions to comply with accounting practices. Additionally, interpreting the results can be more easily tied to the characteristics of the securities and the stress test scenarios. Also, this approach would more accurately reflect the income impact of securities characteristics within a stress test scenario. These instrument-specific characteristics cannot be inferred from prior observations of aggregate income on securities by type as reported in FR Y-9C. As a result, these items would not be captured accurately by the previous regression models. The Board is also proposing changes to FR Y-14Q, Schedule B as discussed in a later section. This change would enable the Board to calculate hedge income by the structural, calculation-based approach in line with the interest income on the securities being hedged.

<!-- Source PDF page 191 -->

<a id="sec-178"></a>

##### (a) Model Specification

The model calculates interest income for any security *i* and derivative *d* at time *t* as follows:

**Equation A40** – Interest Income on U.S. Treasuries Projection

$$Interest\ Income_{i,t} = Coupon\ Accrual_{i,t} + AccretionAmortization_{i,t} + Hedge\ Income_{d,t}$$

*where:*

- $Coupon\ Accrual_{i,t} = Current\ Face\ Value_{i,t} \times \frac{Coupon\ Rate_{i,t}}{4}$;
- $AccretionAmortization_{i,t} = \frac{Current\ Face\ Value_{i,t=0} - Amortized\ Cost_{i,t=0}}{Maturity\ in\ Quarter_{i,t=0}}$; and
- $Hedge\ Income_{d,t} = Notional\ Amount_{d,t} \times \frac{Pay\ Rate_{d,t} - Receive\ Rate_{d,t}}{4}$.

<!-- page 192 -->

Coupon accrual is calculated using the beginning-of-the-period current face value at time *t* and the coupon rate of the bond in question. The Board uses vendor data to source coupon rates, which in some cases may not be available.

Accretion/Amortization is calculated to account for the pull-to-par of the amortized cost of the security and its impact on income. Accretion/Amortization is calculated using the straight-line method for this subset of securities.

Hedge income is calculated to account for the impact of qualifying accounting hedges associated with a security and its impact on income. Form FR Y-14Q, Schedule B.2 provides information on qualifying accounting hedges associated with securities. However, the current schedule does not report the information needed to calculate hedge income. As a result, the initial assumption for $Hedge\ Income_{d,t}$ will be zero.| A new FR Y-14Q, Schedule B.2 and FR Y14-Q, Schedule B.3 are proposed which have the necessary fields, including both fixed- and floating-leg details for swaps. To the extent that the contemplated changes to FR Y-14Q, Schedule B.2 are accepted, the new reporting elements would enable the Board to calculate hedge income as detailed in the formula above. If a qualified accounting hedge is associated with multiple securities, such as the Portfolio Layer Method fair value hedge, that derivative’s income impact will be calculated separate from any security and added to the firm-level aggregate interest income for the securities type most prevalent in the closed portfolio. The Board discusses collecting and incorporating data on interest rate risk hedges in a later section in this document.

After accounting for the three components listed above, the model also incorporates the maturity of securities. To maintain a constant balance assumption, the Board uses a reinvestment assumption. Reinvestments represent securities purchased during the projection horizon to
<!-- page 193 -->

replace those securities that paydown during the projection quarters. The same reinvestment assumption is used across both the interest income on securities models and the Securities Model.[^64] For additional details on the reinvestment assumptions, please refer to the Securities Model Description. For the purposes of coupon accrual, the Board assumes that all purchases in future quarters are made on the first day of the subsequent quarter to the maturing quarter of the security.

<!-- Source PDF page 193 -->

<a id="sec-179"></a>

##### (b) Assumptions and Limitations

The proposed model for estimating interest income on U.S. Treasuries makes various assumptions and has a number of limitations. One of the key limitations of the proposed approach is the lack of data on the income impact of hedges. For example, it is common practice for firms to enter into pay-fixed swaps to hedge fair value changes of Treasury securities. These hedges change the income stream to that of a floating instrument. Qualified accounting hedges can dramatically change the income profile of securities. While qualified accounting hedges against securities held in the investment portfolio are reported in FR Y-14Q, Schedule B.2, the current data attributes reported within this schedule do not allow for independent calculation. There are no data elements that provide the terms of either the fixed or floating legs for swaps. If the changes proposed to the FR Y-14Q, Schedules B.2 and B.3 are not implemented, the Board will need to identify other alternative data sources to account for the hedge impact on interest income.

The reinvestment assumption can have a material impact on interest income on securities. The characteristics of securities assumed to be purchased over the forecast horizon can change the level of income. In particular, the choice not to apply hedges against reinvestments and the
<!-- page 194 -->

coupon type (i.e., fixed/floating) of those reinvestments have an outsized impact on income model results.

There are a variety of other items related to securities and hedging that impact interest income, which the proposed model described above does not incorporate. One of these items is the impact on income from other comprehensive income (OCI) releases from securities previously transferred from available for sale (AFS) to held-to-maturity (HTM). Another item is the income impact from previously terminated hedges as discussed in more detail in the section on proposed treatment of interest rate risk hedges in the suite of models for pre-provision net revenue.

<!-- Source PDF page 194 -->

<a id="sec-180"></a>

##### (c) Questions

The Board is requesting public input on this proposed model for interest income on U.S. Treasuries, including, but not limited to, input on the following questions:

*Question A161: The Board seeks comment on the proposed approach to model interest income on U.S. Treasuries, as compared to the Board's current panel regression model.*

*Question A162: The amortized cost reported in FR Y-14Q, Schedule B.1 can be reported as an adjusted number, especially in cases where the security has an associated qualified accounting hedge. Should the Board make any adjustments to the amortized cost reporting in the FR Y-14Q, Schedule B.1 to get a better calculation of accretion/amortization?*

*Question A163: Do the new fields proposed in the revisions to FR Y-14Q, Schedules B.2 and B.3 pose any issues when calculating hedge income impacts as detailed in the model calculation above?*

*Question A164: Please provide comments on the proposed reinvestment strategy detailed within the Securities Model Description and its impact on interest income on securities.*
<!-- page 195 -->

<!-- Source PDF page 195 -->

<a id="sec-181"></a>

#### (4) Interest Income on Mortgage-Backed Securities

The Board proposes an alternative structural approach to model interest income on mortgage-backed securities that is based on security-level microdata available in form FR Y-14Q, Schedule B. The approach relies on calculating interest income based on the sum of (a) coupon accruals for securities, (b) the amortization/accretion of amortized cost, and (c) the income impacts from any qualifying accounting hedges associated with the security. The Board uses bond-specific details from FR Y-14Q, Schedule B.1 along with vendor data, including coupon rate and maturity. Certain simplifying assumptions or adjustments are made due to lack of information regarding either the security or hedging instrument in question. For this securities category, the Board uses a vendor model to account for the prepayment behavior of residential mortgage-backed bonds.

There are multiple benefits to using this calculation-based approach rather than the regression models described earlier in this document. While straightforward, this approach is closer to the business-as-usual calculations performed by institutions to comply with accounting practices. Additionally, interpreting the results can be more easily tied to the characteristics of the securities, the underlying interest rate risk hedges, and the stress testing scenario in question. This approach would more accurately reflect the income impact of securities and the underlying accounting hedge characteristics for a given stress testing scenario. The Board cannot infer these instrument-specific characteristics from prior observations of aggregate income on securities by type as reported in FR Y-9C.
<!-- page 196 -->

<!-- Source PDF page 196 -->

<a id="sec-182"></a>

##### (a) Model Specification

The model calculates interest income for any security *i* and derivative *d* at time *t* as follows:

**Equation A41** – Interest Income on Mortgage-Backed Securities Projection

$$Interest\ Income_{i,t} = Coupon\ Accrual_{i,t} + AccretionAmortization_{i,t} + Hedge\ Income_{d,t}$$

*where*

- $Coupon\ Accrual_{i,t} = Current\ Face\ Value_{i,t} \times \frac{Coupon\ Rate_{i,t}}{4}$;
- $AccretionAmortization_{i,t} = \frac{Current\ Face\ Value_{i,t} - Amortized\ Cost_{i,t}}{4 * Weighted\ Average\ Life_{\,i,t=0}}$; and
- $Hedge\ Income_{d,t} = Notional\ Amount_{d,t} \times \frac{Pay\ Rate_{d,t} - Receive\ Rate_{d,t}}{4}$.

In the case of Agency residential mortgage-backed securities, a vendor model is used to calculate the income to better reflect the impacts of prepayments. This vendor model is used across both interest income on securities as well as the Securities Model.[^65]

For all other mortgage-backed securities, coupon accrual is calculated using the beginning-of-the-period current face value at time t and the coupon rate of the bond in question. The coupon rate is sourced from vendor data and in some cases may not be available. To the extent that the coupon rate is not available, the book yield report in the FR Y-14Q, Schedule B.1 will be used. In the case of zero-coupon bonds, the security is assumed to accrue at the book yield. In the case of floating-rate securities, data on margin is not available. As a result, the model will impute the margin assuming an index of the 3-month Treasury. To do this, the *t*=0 coupon rate will be used along with the *t*=0 spot 3-month Treasury rate to infer a margin. That inferred margin will then be added to the spot 3-month Treasury rate applicable in all forward quarters.
<!-- page 197 -->

For any securities other than Agency residential mortgage-backed securities, the Board does not propose to model prepayments because these securities are mostly commercial mortgage-backed securities which are expected to have low or no prepayments.

Accretion/amortization is calculated to account for the pull-to-par of the amortized cost of the security and its impact on income. For Agency residential mortgage-backed securities, the straight-line method is used, leveraging the *t*=0 Weighted Average Life.

For all other mortgage-backed securities, accretion/amortization is calculated using the effective interest method for this subset of securities. It is assumed that both the coupon rate and the book yield remain constant throughout the life of the security. If either the coupon rate or book yield data is not available, a straight-line approach will be used for accretion/amortization amounts.

Hedge income is calculated to account for the impact of qualifying accounting hedges associated with a security and its impact on income. FR Y-14Q, Schedule B.2 provides information on qualifying accounting hedges associated with securities. However, the current schedule does not report the information needed to calculate hedge income. As a result, the initial assumption for $Hedge\ Income_{d,t}$ will be zero.| A new FR Y-14Q, Schedule B.2 and B.3 is proposed which has the necessary fields, including both fixed- and floating-leg details for swaps.

To the extent that the proposed changes to the FR Y-14Q, Schedule B.2 are accepted, the new reporting elements would enable the Board to calculate hedge income as detailed in the formula above. If a qualified accounting hedge is associated with multiple securities, such as a Portfolio Layer Method fair value hedge, that derivative’s income impact will be calculated separate from any security and added to the firm-level aggregate interest income for the securities type most prevalent in the closed portfolio.
<!-- page 198 -->

After accounting for the three components listed above, the model also incorporates the maturity of securities. To maintain a constant balance assumption, a reinvestment assumption is used. Reinvestments represent securities purchased during the projection horizon to replace those securities with paydown during the projection quarters. The same reinvestment assumption is used across both the interest income on securities models and the Securities Model. For the purposes of coupon accrual, the Board assumes that all purchases in future quarters are made on the first day of the quarter subsequent to the maturing quarter of the security.

<!-- Source PDF page 198 -->

<a id="sec-183"></a>

##### (b) Assumptions and Limitations

The proposed model for estimating interest income on mortgage-backed securities makes various assumptions and has a number of limitations.

One of the key limitations of this approach is the lack of data on the income impact of hedges. For example, it is common practice for firms to enter into pay-fixed swaps to hedge fair value changes of mortgage-backed securities. This changes the income stream to that of a floating instrument. Qualified accounting hedges can dramatically change the income profile of securities. While qualified accounting hedges against securities held in the investment portfolio are reported in FR Y-14Q, Schedule B.2, the current data attributes reported within this schedule do not allow for independent calculation. There are no data elements that provide the terms of either the fixed or floating leg for swaps. If the changes proposed to FR Y-14Q, Schedule B.2 and B.3 are not implemented, the Board will need to identify other alternative data sources to account for the hedge impact on interest income.

The reinvestment assumption can have a material impact on interest income on securities. The characteristics of securities assumed to be purchased over the forecast horizon can change
<!-- page 199 -->

the level of income. In particular, the choice not to apply hedges against reinvestments and the coupon type (i.e., fixed/floating) of those reinvestments have an outsized impact on income model results. Given limitations regarding securities data from vendors, the Board does not have reliable margin information for all floating rate instruments (except for Agency residential mortgage-backed securities). As a result, an assumption is made that all floating instruments are indexed to the 3-month Treasury rate. This could be impactful for securities indexed to longer tenor rates or rates other than Treasuries.

This model relies on a vendor model for prepayment behavior on Agency residential mortgage-backed securities.

The model assumes no prepayment for securities other than Agency residential mortgage-backed securities. This could dampen the impact of scenario rate paths on interest income on mortgage-backed securities projections and assume existing securities remain on balance sheets for longer than otherwise expected.

There are a variety of other items related to securities/hedges which impact interest income, which the proposed model does not incorporate. One of these items is the impact on interest income from other comprehensive income (OCI) releases from securities previously transferred from available for sale (AFS) to held-to-maturity (HTM). Another item is the income impact from previously terminated hedges.

<!-- Source PDF page 199 -->

<a id="sec-184"></a>

##### (c) Questions

The Board is requesting public input on this proposed model for interest income on mortgage-backed securities, including, but not limited to, input on the following questions:
<!-- page 200 -->

*Question A165: The Board seeks comment on the proposed approach to model interest income on mortgage-backed securities, as compared to the Board's current panel regression model.*

*Question A166: The amortized cost reported in FR Y-14Q, Schedule B.1 can be reported as an adjusted number, especially in cases where the security has an associated qualified accounting hedge. Should the Board make any adjustments to the reported amortized cost reporting in the FR Y-14Q, Schedule B.1 to get a better calculation of accretion/amortization?*

*Question A167: Do the new proposed fields in the FR Y-14Q, Schedules B.2 and B.3 pose any issues when calculating hedge income impacts as detailed in the model calculation above?*

*Question A168: Please provide comments on the proposed reinvestment strategy (detailed within the Securities Model Description) and its impact on interest income on mortgage-backed securities.*

<!-- Source PDF page 200 -->

<a id="sec-185"></a>

#### (5) Interest Income on Other Securities

The Board is considering an alternative structural approach to model interest income on other securities that is based on the security level microdata available in form FR Y-14Q, Schedule B. The approach relies on calculating interest income based on the sum of (a) coupon accruals for securities, (b) the amortization/accretion of amortized cost, and (c) the interest income impacts from any qualifying accounting hedges associated with the security. The Board uses bond-specific details, including rate and maturity from FR Y-14Q, Schedule B.1 along with vendor data. The Board makes certain simplifying assumptions or adjustments due to lack of information regarding either the security or the hedging instrument in question.
<!-- page 201 -->

There are multiple benefits to using the structural, calculation-based approach rather than the regression models currently adopted to calculate stress test projections. While simplistic, this structural approach is closer to the business-as-usual calculations performed by institutions to comply with accounting practices. Additionally, interpreting the results can be more easily tied to the characteristics of the securities, accounting hedges, and the stress test scenarios. Also, this approach would more accurately reflect the income impact of securities and hedge characteristics within a stress test scenario. These instrument-specific characteristics cannot be inferred from prior observations of aggregate income on securities by type as reported in FR Y-9C. As a result, these items would not be captured accurately by the previous regression models.

<!-- Source PDF page 201 -->

<a id="sec-186"></a>

##### (a) Model Specification

The model calculates interest income for any security *i* and derivative *d* at time *t* as follows:

**Equation A42** – Interest Income on Other Securities Projection

$$Interest\ Income_{i,t} = Coupon\ Accrual_{i,t} + AccrectionAmortization_{i,t} + Hedge\ Income_{d,t}$$

*where*

- $Coupon\ Accrual_{i,t} + AccrectionAmortization_{i,t} = Amortized\ Cost_{i,t} \times \frac{Book\ Yield_{i,t}}{4}$; and
- $Hedge\ Income_{d,t} = Notional\ Amount_{d,t} \times \frac{Pay\ Rate_{d,t} - Receive\ Rate_{d,t}}{4}$.

The Board uses the book yield reported in the FR Y-14Q, Schedule B.1. In the case of floating rate securities, data on margins is not available. As a result, the Board proposes to impute the margin by assuming a 3-month Treasury index. The Board uses the *t*=0 coupon rate along with the *t*=0 spot 3-month Treasury rate to infer a margin. That inferred margin is then added to the spot 3-month Treasury rate applicable in all forward quarters.
<!-- page 202 -->

There are many securities in this category that are expected to have prepayment in advance of final maturity. Given the broad number of asset classes and security types within this category, it is difficult to model all prepayment characteristics. As a result, no prepayments are modeled on securities within this category.

Accretion/amortization is calculated to account for the pull-to-par of the amortized cost of the security and its impact on income. For this subset of securities, the Board calculates accretion/amortization using the effective interest rate method. The Board assumes that both the coupon rate and the book yield remain constant throughout the life of the security. If either the coupon rate or book yield data is not available, the Board uses a straight-line approach for computing accretion/amortization amounts.

Hedge income is calculated to account for the impact of qualifying accounting hedges associated with a security and its impact on interest income. FR Y-14Q, Schedule B.2 provides information on qualifying accounting hedges associated with securities. However, the current schedule does not report the information needed to calculate hedge income. As a result, the initial assumption for $Hedge\ Income_{d,t}$ will be zero.| In the Securities Model Description, a new FR Y-14Q, Schedule B.2 and B.3 is proposed, which has the necessary fields including both fixed and floating leg details for swaps. To the extent that the proposed changes to FR Y-14Q, Schedule B.2 are accepted, the new reporting elements would enable the Board to calculate hedge income as detailed in the formula above. If a qualified accounting hedge is associated with multiple securities, such as a Portfolio Layer Method fair value hedge, that derivative’s income impact will be calculated separate from any security and added to the firm-level aggregate interest income for the securities type most prevalent in the closed portfolio.
<!-- page 203 -->

After accounting for the three components listed above, the model also incorporates the maturity of securities. To maintain a constant balance assumption, a reinvestment assumption is used. Reinvestments represent securities purchased during the projection horizon to replace those securities with paydown during the projection quarters. The same reinvestment assumption is used across both the interest income on securities models and the Securities Model. For additional details on the reinvestment assumptions, please refer to the Securities Model Description. For the purposes of coupon accrual, the Board assumes that all purchases in future quarters are made on the first day of the quarter subsequent to the maturing quarter of the security.

<!-- Source PDF page 203 -->

<a id="sec-187"></a>

##### (b) Assumptions and Limitations

There are various assumptions and limitations to the proposed model for interest income on other securities. One of the key limitations of this approach is the lack of data on the interest income impact of qualified accounting hedges. For example, it is common practice for firms to enter into pay-fixed swaps to hedge fair value changes of the underlying securities being hedged. This changes the income stream to that of a floating instrument. Qualified accounting hedges can dramatically change the income profile of securities. While qualified accounting hedges against securities held in the investment portfolio are reported in FR Y-14Q, Schedule B.2, the current data attributes reported within this schedule do not allow for independent calculation. There are no data elements that provide the terms of either the fixed or floating legs for swaps. If the changes proposed to the FR Y-14Q, Schedule B.2 and B.3 are not implemented, the Board will need to identify other alternative data sources to account for the hedge impact on interest income.
<!-- page 204 -->

The reinvestment assumption can have a material impact on interest income on securities. The characteristics of securities assumed to be purchased over the forecast horizon can change the level of income. In particular, the choice not to apply qualified accounting hedges against reinvestments and the coupon type (i.e., fixed/floating) of those reinvestments has an outsized impact on interest income model results.

Given limitations regarding securities data from vendors, the Board does not have reliable margin information for all floating rate instruments. As a result, an assumption is made that all floating instruments are indexed to the 3-month Treasury rate. This could be impactful for securities indexed to longer tenor rates or rates other than Treasuries.

The model assumes no prepayment for securities in this category. This could dampen the impact of the stress test scenario rate paths on income projects and assume the full balance of existing securities remain on the balance sheet longer than otherwise expected. If prepayments were modeled, the principle paydowns would be reinvested according to the reinvestment assumptions of the Securities model and would likely earn a lower rate of interest than the reported security.

There are a variety of other items related to securities and their underlying qualified accounting hedges which impact interest income and that the proposed model does not incorporate. One of these items is the impact on interest income from other comprehensive income (OCI) releases from securities previously transferred from available for sale (AFS) to held-to-maturity (HTM). Another item is the interest income impact from previously terminated hedges.
<!-- page 205 -->

<!-- Source PDF page 205 -->

<a id="sec-188"></a>

##### (c) Questions

The Board is requesting public input on this proposed model for interest income on other securities, including, but not limited to, input on the following questions:

*Question A169: The Board seeks comment on the proposed approach to model interest income on other securities, as compared to the Board's current panel regression model.*

*Question A170: Are there other items that the Board should consider when modeling interest income on other securities?*

*Question A171: Are the model’s assumptions around floating rate securities reasonable? How else could the Board account for these assumptions?*

*Question A172: The amortized cost reported in FR Y-14Q, Schedule B.1 can be reported as an adjusted number, especially in cases where the security has an associated qualified accounting hedge. Should the Board make any adjustments to the amortized cost reporting in the FR Y-14Q, Schedule B.1 to get a better calculation of accretion/amortization?*

*Question A173: Do the new proposed fields in the FR Y-14Q, Schedules B.2 and B3 pose any issues when calculating qualified accounting hedge income impacts as detailed in the model calculation above?*

*Question A174: Please provide comments on the proposed reinvestment strategy (detailed within the Securities Model Description) and its impact on interest income on other securities.*

<!-- Source PDF page 205 -->

<a id="sec-189"></a>

#### (6) Interest Income on Other Interest/Dividend-Bearing Assets

The Board proposes a structural approach to model interest income from other interest/dividend-bearing assets. Interest income from other interest/dividend-bearing assets consists of interest earned on federal funds sold and securities purchased under agreements to
<!-- page 206 -->

resell, as well as interest and dividends on other assets, such as the Federal Reserve or Federal Home Loan Bank stock.

The relevant balances for this component are the assets reported in line item 15 of the Net Interest Income Worksheet of FR Y-14Q, Schedule G (G.2). The portion of the portfolio that is federal funds sold and securities purchased under agreements to resell has short duration and is directly linked to short term interest rates. This portion can be quantified by utilizing the additional fields provided by the firms in the footnotes to the worksheet and by cross-referencing with the balances reported in FR Y-9C (BHCK3365). Federal funds sold and securities purchased under agreements to resell comprise most of other interest/dividend-bearing assets reported in FR Y-14Q.

<!-- Source PDF page 206 -->

<a id="sec-190"></a>

##### (a) Model Description

Under this structural approach, interest income for this component at each quarter of the projection is calculated starting from a simple and intuitive assumption: the federal funds sold and securities purchased under agreements to resell earn a yield that responds directly to the short-term interest rate, as this is consistently observed in historical data. In particular, the Board assumes that the yield on this component is the 3-month U.S. Treasury rate. The remaining assets of this portfolio are assumed to earn a yield that responds to longer-term rates captured by the 10-year U.S. Treasury rate to account for assets with longer maturity or higher yields.[^66]

More formally, let *αb* be the proportion of assets consisting of federal funds sold and securities purchased under agreements to resell for each firm *b, Bb* be the total balance on other interest/dividend bearing assets, and *Fb* be the income earning from this component. Then, for each firm *b* at any quarter *t*:
<!-- page 207 -->

**Equation A43** – Interest Income on Other Interest/Dividend-Bearing Assets

$$F_{b,t} = \alpha_{b,t}B_{b,t}Treasury3m + (1 - \alpha_{b,t})B_{b,t}Treasury10y$$

*where*

- $Treasury3m$ is the 3-month Treasury yield; and
- $Treasury10y$ is the 10-year Treasury yield.

Using this equation for the projection period, the projected flow of income $F_{b,q}$, for firm $b$ in quarter $q$ over the projection horizon, can be calculated as:

$$F_{b,q} = \alpha_{b,q}B_{b,q}Treasury3m_q + (1 - \alpha_{b,q})B_{b,q}Treasury10y_q$$

The stress test assumes constant balances for all firms; therefore, $B_{b,q} = B_{b,q0}$ for all quarters where $B_{b,q0}$ represents the balances of firm $b$ at lift-off quarter $q0$. This means that the projected flow of income is calculated based on the balances at the start of the projection horizon. The share $\alpha_{b,q} = \alpha_{b,q0}$ is also assumed to stay constant over the projection quarters.

<a id="sec-191"></a>

##### (b) Assumptions and Limitations

When using the structural model, the Board makes the assumption that the yield each firm earns over the projection horizon is given by the 3-month U.S. Treasury rate for the portion of the portfolio that consists of the federal funds sold and securities purchased under agreements to resell, and given by the 10-year U.S. Treasury rate for the remainder of the portfolio. While the 3-month U.S. Treasury rate tracks the overnight and other short-term lending rates closely, some fluctuations may be observed, especially when the short-term lending is collateralized by special or rare securities. Similarly, the remainder of each firms’ portfolio may exhibit heterogeneity and earn a rate that is higher or lower than the 10-year U.S. Treasury rate. However, this portion of the portfolio is relatively small, and alternative rates do not result in material differences in the projected income.
<!-- page 208 -->

The Board determined that the structural model described above had several advantages over a panel regression framework, including enhanced clarity and explainability as well as simplicity (since it does not involve coefficients estimation). Structural models avoid statistical estimation, meaning that the variability of projections over stress testing cycles can be fully explained by reported balances for each bank, and by the variation in the interest rate scenario paths. In addition, due to firm discretion, and consistent with the accounting rules on balance sheet offsetting, some firms may report their balances or income on a gross or net basis. Due to lack of consistency in firm reporting, this could produce less precise projections when a regression approach is adopted.

The Board proposes to model interest income on other interest/dividend-bearing assets as one component that consists of several categories of interest income earned on interest-earning assets. The Board chose this approach due to data limitations when identifying these components using FR Y-14Q reporting schedules.

<!-- Source PDF page 208 -->

<a id="sec-192"></a>

##### (c) Questions

The Board is requesting public input on this proposed model for interest income on other interest/dividend-bearing assets, including, but not limited to, input on the following question:

*Question A175: The Board seeks comment on the proposed approach to model interest income on other interest/dividend-bearing assets, as compared to the Board's current panel regression model.*

*Question A176: The Board is proposing modeling interest income from federal funds sold and securities purchased under agreement to resell jointly with other interest/dividend-earning assets using a structural model. What are the advantages or disadvantages of modeling these components together?*
<!-- page 209 -->

<!-- Source PDF page 209 -->

<a id="sec-193"></a>

#### (7) Interest Expense on Domestic Time Deposits

The Board proposes a structural model as an alternative specification for interest expense on domestic time deposits. The model assumes a fraction of the firm’s domestic time deposit portfolio matures each period. Maturing balances are replaced with new funding each period priced to a reference rate. The remaining fraction of the firm’s portfolio receives the rate paid on domestic time deposits in the previous period. The dependent variable in the model is the domestic time deposit rate as reported in the FR Y-14Q. Interest expense on domestic time deposits is computed by multiplying the modeled rate by the average balance on domestic time deposits as reported in the FR Y-14Q.

<!-- Source PDF page 209 -->

<a id="sec-194"></a>

##### (a) Model Specification

The model is specified according to the following equation:

**Equation A44** – Interest Expense on Domestic Time Deposits Rate Projection

$$Rate_{b,t} = \rho_b * Treasury1y_t + (1 - \rho_b) * Rate_{b,t-1}$$

*where*

- $Rate_{b,t}$ is the rate paid on domestic time deposits by firm $b$ at quarter $t$;
- $\rho_b \equiv \frac{1}{WAL_b}$: is the fraction of the portfolio that reprices every period (quarter). $WAL_b$ is the weighted average life of domestic time deposits for firm $b$; and
- $Treasury1y_t$: is the 1-year Treasury yield at quarter $t$.

The initial rate paid on domestic time deposits is the average rate paid on domestic time deposits in the jump-off quarter as reported in the FR Y-14Q, Schedule G, line item 42E (Time Deposits). The fraction of the portfolio which reprices each period is computed as one divided by the Weighted Average Life of the portfolio as reported by firms in the FR Y-14Q, Schedule G, line item 71 (Domestic Deposits – Time). This fraction is reflective of the portfolio’s maturity profile and remains constant throughout the projection.
<!-- page 210 -->

<!-- Source PDF page 210 -->

<a id="sec-195"></a>

##### (b) Assumptions and Limitations

A structural model specification necessarily requires assumptions about future behavior. First, a constant percentage of the portfolio is assumed to be repriced every period. This assumption abstracts from the heterogeneity of the rate and maturity profile in a firm’s time deposit portfolio. Using only one piece of information about maturity profiles, the Weighted Average Life, necessitates this simplifying assumption.

A second assumption is that all re-originated time deposits are priced at the 1-year Treasury yield. In this model, firms do not have market power in time deposit pricing. The only difference in the level of rates throughout the projection period comes from the rate paid on domestic time deposits at lift-off and the firm-specific Weighted Average Life. Assuming all re-originations are paid, the 1-year Treasury yield also ignores the heterogeneity in rates that comes with the origination of new time deposits.

A limitation of the model is that richer maturity structures are not possible. Time deposits have contractual maturities that do not factor into this mechanism. For example, a time deposit balance that reprices to the 1-year Treasury yield in one quarter is as equally likely to be repriced in the following quarter as any other time deposit. There is no mechanism for the time deposit balance to be held for the contractual term. The use of data on the maturity profile of time deposits may address the lack of maturity structure in this model. For example, Call Reports contain information on the quantity of domestic time deposits due to mature in 1-quarter, 1-year, and 3-years. The above model can be modified to assume that fixed amounts of time deposits mature each quarter based on maturity profile information. Under this modification, when a balance matures, it is repriced to a reference rate and unmatured balances continue to receive the original rate paid by the firm on time deposits. This alternative specification could address the
<!-- page 211 -->

limitation described above by introducing heterogeneity in time deposit maturities and rates, but as a trade-off it entails further data processing and increased model complexity.

<!-- Source PDF page 211 -->

<a id="sec-196"></a>

##### (c) Questions

The Board is requesting public input on this proposed model for interest income on domestic time deposits, including, but not limited to, input on the following question:

*Question A177: The Board seeks comment on the proposed approach to model interest expense on domestic time deposits, as compared to the Board's current panel regression model.*

<!-- Source PDF page 211 -->

<a id="sec-197"></a>

#### (8) Interest Expense on Other Domestic Deposits

The Board proposes a structural model as an alternative for interest expense on other domestic deposits, using as a data source the interest rates on subcomponents of domestic deposits reported in form FR Y-14Q. These FR Y-14Q subcomponents are money market accounts, savings accounts, and transaction accounts (negotiable order of withdrawal [NOW], automatic transfer service [ATS], and other accounts). The model is split into two regimes, each with its own model specification, depending on the level of the 3-month Treasury yield in a particular projection quarter. The effective lower-bound period occurs when the 3-month Treasury yield is below 25 basis points in a projection quarter. The non-effective lower bound occurs when the 3-month Treasury yield is above 25 basis points in a projection quarter.

In the non-effective lower-bound regime, the interest rate on deposits is equal to the previous period interest rate plus the change in the 3-month Treasury yield multiplied by a coefficient named “beta”. The beta is given by the median of firm-reported betas, sourced from the Y-14Q, Schedule G, corresponding to the direction of the 3-month Treasury yield movement. If the computed deposit interest rate falls below an assumed floor, the deposit rate is set to the
<!-- page 212 -->

assumed floor. In the effective lower-bound regime, the interest rate on deposits is equal to the 3-month Treasury yield plus a firm-specific spread.

<!-- Source PDF page 212 -->

<a id="sec-198"></a>

##### (a) Model Specification

Each individual subcategory of other domestic deposits reported in the FR Y-14Q (money market accounts, savings accounts, and transaction accounts) is modeled separately and then aggregated. The model is split into two regimes: one during an effective lower-bound period defined as the 3-month Treasury yield being below 25 basis points, and one during a non-effective lower-bound period. The general model is specified according to the following equation during the effective lower-bound period:

**Equation A45** – Interest Expense on Other Domestic Deposits Rate Projection, Effective Lower

Bound Period

$$Rate_{i,b,t} = floor_{i,b,t}$$

*where:*

- $i \in (MMA, Savings, Transaction)$;
- $b$ indicates the firm;
- $t$ indicats the quarter;
- $floor_{i,b,t} = Treasury3m_t + Spread_{i,b}$;
- $Spread_{i,b}$ is the firm- and deposit-type-specific spread to the 3-month Treasury yield during an effective lower bound period; and
- $Treasury3m_t$ is the 3-month Treasury yield.

The firm-specific spread to the 3-month Treasury yield is empirically estimated as the average distance between the deposit rate paid by the firm during the most recent effective lower-bound period. Following the definition assumed above, the most recent effective lower-bound period occurred from 2020:Q2 to 2021:Q4.

During a non-effective lower bound period ($Treasury3m_t > 25bps$) the general model specification is:

<!-- page 213 -->

**Equation A46** – Interest Expense on Other Domestic Deposits Rate Projection, Non-Effective

Lower Bound Period

$$Rate_{i,b,t} = \max\left(Rate_{i,b,t-1} + \delta_{i,t},\ assumed\_floor_{i,b}\right)$$

*where:*

- $i \in (MMA, Savings, Transaction)$;
- $\delta_{i,t} = \max(\Delta Treasury3m_t, 0) * \beta_i^{up} + \min(\Delta Treasury3m_t, 0) * \beta_i^{down}$;
- $\Delta Treasury3m_t$ is the change in the 3-month Treasury yield;
- $\beta_i^{up}$ and $\beta_i^{down}$ are the constant betas for the up and down rate respectively;
- $assumed\_floor_{i,b} = First\_ELB\_Treasury3m + Spread_{i,b}$;
- $Spread_{i,b}$ is the firm- and deposit-type-specific spread to the 3-month Treasury yield during an effective lower bound period; and
- $First\_ELB\_Treasury3m$ is the minimum between 25 basis points and the first observation of the 3-month Treasury yield which goes below the 25 basis points in the scenario (if available).

The interest rates on money market accounts, savings accounts, and transaction accounts are retrieved from the Y-14Q, Schedule G, line items 42B, 42C, and 42D, respectively. The up and down rate betas are retrieved from the Y-14Q, Schedule G, line items 79A, 79B, 80A, 80B, 81A, and 81B. The beta used in the model is the median of the firm-reported betas for the respective deposit category at lift-off. The reasons for using a median beta are both to mitigate the reliance on individual firm-provided estimates, as well as to address outliers in the data.

The interest rate on other domestic deposits is aggregated up from the subcomponents as follows:

**Equation A47** – Interest Rate on Other Domestic Deposits Aggregation

$$Rate_{b,t} = \left(\sum_i Rate_{i,b,t} * Balance_{i,b,t}\right) / \left(\sum_i Balance_{i,b,t}\right)$$

*where:*

- $i \in (MMA, Savings, Transaction)$; and
- $Balance_{i,b,t}$ is the balance reported in the Y-14Q corresponding to the rate $i$ for firm $b$ at time $t$.

<!-- page 214 -->

The aggregate interest rate on other domestic deposits is then multiplied by the average balance on other domestic deposits as reported in the FR Y-14Q to produce the interest expense on other domestic deposits.

<!-- Source PDF page 214 -->

<a id="sec-199"></a>

##### (b) Assumptions and Limitations

An assumption is that the effective lower bound occurs when the three-month Treasury yield falls below 25 basis points. This is consistent with the lowest observed historical policy target range for the federal funds rate of 0–25 basis points. The 3-month Treasury yield is commonly used as the quarterly proxy for the risk-free rate.

A second assumption is that non-effective lower-bound periods are treated as normal periods. This abstracts from the relative distance of deposit rates to the effective lower bound where yield compression can occur. A third assumption is that during non-effective lower-bound periods, a firm’s rate floor is the first observation of the 3-month Treasury yield that goes below 25 basis points in the scenario or 25 basis points. This assumption eliminates the possibility that the rate on other domestic deposits will go below the assumed floor during the non-effective lower-bound period.

A third assumption of the model is the use of a constant beta, taken as the median of firm-reported betas, for all firms. By construction, this eliminates the possibility of considering market power in the pricing of non-time deposits. Additionally, this assumption abstracts from time variation in betas which has been noted in academic literature and is observed in the firm’s reporting of betas.
<!-- page 215 -->

<!-- Source PDF page 215 -->

<a id="sec-200"></a>

##### (c) Questions

The Board is requesting public input on this proposed model for interest expense on other deposits, including, but not limited to, input on the following questions:

*Question A178: The Board seeks comment on the proposed approach to model interest expense on other deposits, as compared to the Board's current panel regression model.*

<!-- Source PDF page 215 -->

<a id="sec-201"></a>

#### (9) Interest Expense on Foreign Deposits

The Board proposes an alternative model for interest expense on foreign deposits, which is very similar to the alternative model for other domestic deposits previously described. The data for foreign deposits is retrieved from the Y-14Q and the quantities are equivalent to those retrieved from the FR Y-9C. Aggregate foreign deposits have a smaller impact with respect to the larger categories of domestic time deposits and other domestic deposits.

<!-- Source PDF page 215 -->

<a id="sec-202"></a>

##### (a) Model Specification

The model for foreign deposits is identical to the proposed model for other domestic deposits detailed above with the exception that the subcategories of deposit rates from the Y-14Q are foreign deposits and foreign deposits-time (Schedule G, line items 43A and 44B, respectively). The equivalent balances are retrieved from the Y-14Q to combine foreign non-time deposits and foreign time deposits (Schedule G, line items 35A and 35B, respectively) to an aggregate foreign deposit rate. The up and down rate for betas for foreign deposits are retrieved from the Y-14Q, Schedule G, line items 83A, 83B, 84A, and 84B.

<!-- Source PDF page 215 -->

<a id="sec-203"></a>

##### (b) Assumptions and Limitations

When developing the interest expense on foreign deposits model, the Board assumed that both foreign time and foreign non-time deposits should follow the same model. This decision
<!-- page 216 -->

abstracts from the inherent differences in the contractual characteristics of time and non-time deposits while it prioritizes the Policy Statement principle of simplicity.

A second assumption is that re-originated foreign deposits are priced at the 3-month Treasury yield. This assumption abstracts from the fact that foreign deposits earn a rate more in line with their country of origin. Since there is no data available on the current regulatory forms regarding the country of origin, the Board decided to assume the price is the 3-month Treasury yield for all foreign deposits. This aligns with the scenario, which assumes a worldwide recession in which all central banks lower interest rates substantially. Similarly, there is no consideration of the effect of exchange rates over the scenario.

<!-- Source PDF page 216 -->

<a id="sec-204"></a>

##### (c) Questions

The Board is requesting public input on this proposed model for interest expense on foreign deposits, including, but not limited to, input on the following questions:

*Question A179: The Board seeks comment on the proposed approach to model interest expense on foreign deposits, as compared to the Board's current panel regression model.*

<!-- Source PDF page 216 -->

<a id="sec-205"></a>

#### (10) Interest Expense on Federal Funds Purchased and Securities Sold under the Agreement to Repurchase

The Board proposes an alternative structural approach to model interest expense on federal funds purchased and securities sold under agreements to repurchase.

The liabilities under interest expense on federal funds purchased and securities sold under agreements to repurchase have short durations and are directly linked to short-term interest rates. The relevant balance for this component is the liabilities reported in line items 44A (“federal
<!-- page 217 -->

funds purchased”) and 44B (“securities sold under agreements to repurchase”) of the Net Interest Income Worksheet of FR Y-14Q, Schedule G.

<!-- Source PDF page 217 -->

<a id="sec-206"></a>

##### (a) Model Description

Under this structural approach, interest expense for this component at each projection quarter is calculated starting from a simple and intuitive assumption: the federal funds purchased and securities sold under the agreement to repurchase earn a rate that responds directly to the short-term interest rate, as this is consistently observed in historical data. In particular, the Board assumes that the rate on this component is the 3-month U.S. Treasury rate. This approach is equivalent to the one previously described for interest income on federal funds sold and securities purchased under agreements to resell, except that the federal funds and repo positions on the asset side are subsumed within the component other interest/dividend-bearing assets. For the sake of completeness, it is summarized below.

Let *Bb* be the total balance on federal funds purchased and securities sold under agreements to repurchase, and *Fb* be the expense paid from this component. Then, for each firm *b* at any quarter *t*

**Equation A48** – Interest Expense on Federal Funds Purchased and Securities Sold under the Agreement to Purchase|

$$F_{b,t} = B_{b,t}Treasury3m_t,$$

*where:*

- $Treasury3m$ is the 3-month Treasury yield for quarter $t$.

Using this equation for the projection period, the projected flow of expense $F_{b,q}$, for firm $b$ in quarter $q$ on the projection horizon, thus, can be calculated as:

$$F_{b,q} = B_{b,q}Treasury3m_q.$$

<!-- page 218 -->

The stress test assumes constant balances for all firms; therefore, $B_{b,q} = B_{b,q0}$ for all periods, where $B_{b,q0}$ represents firm’s $b$ balances at lift-off quarter $q0$. This means that the projected flow of expense is calculated based on the balances at lift-off.

<!-- Source PDF page 218 -->

<a id="sec-207"></a>

##### (b) Assumptions and Limitations

When using the structural model, the Board makes the assumptions that the rate each firm earns over the projection horizon is given by the 3-month U.S. Treasury rate. While the 3-month U.S. Treasury rate tracks the overnight and other short-term borrowing rates closely, some fluctuations may be observed, especially when the short-term borrowing is collateralized by special or rare securities.

The Board determined that the structural model described above had several advantages over a panel regression framework, including enhanced clarity and explainability as well as simplicity (since it does not involve coefficients estimation). Structural models avoid statistical estimation, meaning that the variability of projections over stress testing cycles can be fully explained by reported balances for each bank and the variation in the interest rate scenario paths. In addition, due to firm discretion, and consistent with the accounting rules on balance sheet offsetting, some firms may report their balances or income on gross or net basis. Due to lack of consistency in firm reporting, this could produce less precise projections when a regression approach is adopted.

<!-- Source PDF page 218 -->

<a id="sec-208"></a>

##### (c) Questions

The Board is requesting public input on this proposed model for interest expense on federal funds purchased and securities sold under agreements to repurchase, including, but not limited to, input on the following questions:
<!-- page 219 -->

*Question A180: The Board seeks comment on the proposed approach to model interest expense on federal funds purchased and securities sold under agreements to repurchase, as compared to the Board's current model.*

<!-- Source PDF page 219 -->

<a id="sec-209"></a>

### b. Estimated Parameters for Proposed Structural Models

The tables included in this section present the estimated parameters for the structural models proposed for the 2026 stress test. Table A7 presents the median betas for the interest expense on other domestic deposits and for the interest expense on foreign deposits models. Table A8 presents the industry-level scalars to be used in the calculation of projections for interest income on loans. The Board calculated these parameters based on data submitted on Form FR Y-14Q.

**Table A7–** Median Betas for Proposed Deposit Models (Equations A46)

| Deposit Type | Interest Rate Movement | Median Beta |
|---|---|---|
| Other Domestic: Money Market Accounts | Up | 0.620 |
| median_beta_dom_mma_deposit_down | Down | 0.645 |
| Other Domestic: Savings | Up | 0.310 |
| median_beta_dom_savings_deposit_down | Down | 0.335 |
| Other Domestic: Other | Up | 0.465 |
| median_beta_dom_other_trans_deposit_down | Down | 0.490 |
| Foreign: Non-time | Up | 0.890 |
| median_beta_for_nontime_deposit_down | Down | 0.790 |
| Foreign: Time | Up | 1.000 |
| median_beta_for_time_deposit_down | Down | 1.000 |

<!-- page 220 -->

**Table A8** – Scalars for Proposed Interest Income on Loans Model

| Portfolio | Scalar |
|---|---|
| Auto | 0.865 |
| C&I, noncore SME loan and card | 1.033 |
| Credit Card | 0.969 |
| Domestic CRE | 1.081 |
| Mortgage | 1.014 |
| Noncore | 1.072 |
| Rest of wholesale | 1.113 |

<!-- Source PDF page 220 -->

<a id="sec-210"></a>

### c. Proposed Adjustments to Pre-Provision Net Revenue Models to Incorporate the Impact of Interest Rate Risk Hedges

Firms use derivative instruments to hedge their exposure to interest rate risks. Examples of the most common types of derivatives used for this purpose are interest rate swaps, interest rate collars, caps, floors, futures, interest rate lock commitments, and forward sales commitments and swaptions. These hedging derivatives can be classified as accounting hedge derivatives or non-accounting hedge derivatives. Accounting hedge derivatives are those that qualify for hedge accounting treatment by meeting strict accounting designation criteria and are designated as accounting hedges by the firm. Non-accounting hedge derivatives, on the other hand, are derivatives used to mitigate risks without receiving the hedge accounting treatment. Although all derivatives including those underlying interest rate risk hedges are recorded on the balance sheet at fair value, with gains or losses reflected in net income, interest rate risk accounting hedge derivatives are subject to specific accounting models that generally offset the instrument’s changes in fair value against the hedged item’s gains or losses, thereby reducing the volatility of firms’ net income.
<!-- page 221 -->

<!-- Source PDF page 221 -->

<a id="sec-211"></a>

#### (1) Model Specification

The Board is proposing to collect additional data on firms’ interest rate risk hedging positions for accounting hedges as part of FR Y-14Q data collection for Schedule B.2. In particular, the Board proposes to request firms to provide quarterly snapshots of their qualified accounting hedging positions at the end of each quarter, noting which portfolio a given derivative is hedging. The Board also proposes collecting data on the notional amount, derivative type, fix and floating rate details, and maturity. The Board is also considering collecting information on terminated accounting hedges and their impact on existing interest income or expense components at each reporting quarter-end.

Collecting granular data on the underlying accounting hedge positions at each quarter-end will enable the Board to capture the impact of existing hedges, including forward starting hedges, on firms’ interest income and expense during the projection horizon. The Board proposes utilizing the detailed schedule and applying the scenario path of interest rates to measure the impact of existing hedges. The Board does not propose to model hedge renewals or cancellations in light of the overall fixed balance sheet assumption.

The Board also proposes collecting data on accounting interest rate risk hedges that are terminated by the start of the projection horizon as the impact of hedge termination continues to affect interest income or interest expense through the amortization of adjustments over the remaining life of the hedged item. This collection applies only to the hedges whose termination affects interest income or interest expense in any quarter over the projection horizon.

Assuming that the Board can collect data on hedging instruments, the hedge impact for a given component of pre-provision net revenue, where the hedging instrument is an interest rate swap, would be computed as follows:
<!-- page 222 -->

**Equation A49** – Hedge Impact Projection

$$\begin{aligned}Hedge\ Net\ Interest\ Income\ Impact_{PQ} = {} & Accrued\ Interest\ Income_{PQ} - \\ & Accrued\ Interest\ Expense_{PQ},\end{aligned}$$

*where:*

- $Hedge\ Net\ Interest\ Income\ Impact_{PQ}$ is the overall impact on net interest income of accounting interest rate risk hedges in a given projection quarter $PQ$;
- $Accrued\ Interest\ Income_{PQ}$ is the accrued interest either on the fixed or floating rate leg depending on the hedging instrument; and
- $Accrued\ Interest\ Expense_{PQ}$ is the accrued interest expense either on the fixed or floating rate leg depending on the hedging instrument.

The accrued interest on the fixed leg is computed as follows:

**Equation A50** – Accrued Interest Calculation, Fixed Leg

$$Accrued\ Interest_{PQ} = Notional\ Amount \times r \times \frac{N}{360},$$

*where:*

- *r* is the fixed interest rate; and
- *N* is the number of days interest is accrued during the quarter.

The accrued interest on the floating leg is computed as follows:

**Equation A51** - Accrued Interest Calculation, Floating Leg

$$Accrued\ Interest_{PQ} = Notional\ Amount \times (Reference\ Rate + Margin) \times \frac{N}{360},$$

*where:*

- *Reference Rate* is the specified or assumed reference rate (e.g., SOFR or the 3-month Treasury rate);
- *Margin* is the spread over the reference index rate; and
- *N* is the number of days interest is accrued during the quarter. For hedging instruments that use caps or floors, the strike rate details will be incorporated into the calculation of the hedge impact. To model terminated hedges, the Board will spread the cumulative gains or losses from the hedging relationships evenly throughout the remaining maturity of the hedged item.
<!-- page 223 -->

<!-- Source PDF page 223 -->

<a id="sec-212"></a>

#### (2) Assumptions and Limitations

Utilizing granular data on hedge positions will enable the Board to model the direct impact of existing qualified accounting hedges on firms’ interest income and expense positions over the stress test horizon. However, the Board will not make assumptions about future hedge termination or renewal. For example, when moving from a high interest rate environment to a low interest rate environment, the Board will not be able to dynamically capture changes in banks’ balance sheets that will also reflect changes in the hedged positions. Furthermore, the Board will not make assumptions about hedges that might be terminated during the projection horizon to maintain consistency with the overall flat balance sheet assumptions.

<!-- Source PDF page 223 -->

<a id="sec-213"></a>

#### (3) Questions

The Board is requesting public input on this proposed approach for identifying and accounting for the impact of interest rate risk hedging on pre-provision net revenue, including, but not limited to, input on the following questions:

*Question A181: What are the best options to identify and account for the impact of interest rate risk hedging on interest income and interest expenses under stress test scenarios?*

*Question A182: What kind of data collection would this require? In particular, the following questions are relevant:*

*1. What additional data would the Board need to collect from firms to best model the*

*impact of interest rate risk hedges on pre-provision net revenue stress projections?*

*2. Would these data need to include details of the hedged position such as the notional*

*amount, as well as hedging instrument details (such as its derivative type, whether it is*

*fixed or floating rate, and its maturity)?*
<!-- page 224 -->

*3. Would it be feasible for firms to report these types of data to enable the Board to*

*calculate the granular hedge impact?*

*4. What would be the challenges in providing these types of data to the Board on a*

*quarterly basis as part of the Board’s confidential supervisory data collection through*

*FR Y-14?*

*5. Should the Board be incorporating the impact of terminated accounting interest rate*

*risk hedges when making supervisory firm projections?*

*Question A183: Should the Board collect information that decomposes contractual payments for each security from the details related to hedges in order for the Board to estimate firms’ interest income or expense exposure to stress scenarios more precisely?*

*Question A184: Should the Board collect information on terminated accounting hedges?*

*Question A185: The Board is proposing to collect granular data on hedge positions to estimate the impact of hedging on interest income and expense projections. Are there other approaches that the Board should consider? What would the burden be in reporting this granular data?*

*Question A186: The Board proposes requesting quarterly reporting of interest rate risk hedges as part of the updated FR Y-14, Schedule B.2. What would be the relative burden for the firms to report these data quarterly or annually?*

*Question A187: The Board is proposing to take into account only the impact of accounting interest rate risk hedges. Should the Board consider all hedges instead? If so, what data should the Board collect to achieve this?*
<!-- page 225 -->

<!-- Source PDF page 225 -->

<a id="sec-214"></a>

### d. Proposed Regression Models

<!-- Source PDF page 225 -->

<a id="sec-215"></a>

#### (1) Net Interest Income on Trading Assets and Liabilities

The Board proposes an alternative regression approach to model interest income and interest expense on trading assets. Interest income and expense on trading assets are modeled as a single net quantity (interest minus expense), expressed as a ratio normalized by net trading assets (assets minus liabilities). The Board is considering this approach of modeling a single net quantity rather than separate income and expense quantities to avoid challenges in cross-firm comparability that could be introduced by differences in the extent of offsetting used in reporting trading assets and liabilities.

<!-- Source PDF page 225 -->

<a id="sec-216"></a>

##### (a) Model Specification

In the proposed regression model for net interest income on trading assets and liabilities, the ratio for each firm depends on the contemporaneous level of the 3-month Treasury yield and a fixed effect estimated for that firm. Estimation data on firm-level quarterly interest income and expense on trading assets and liabilities, and the associated balances, are sourced from the Net Interest Income Worksheet of the FR Y-14Q, Schedule G. The interest income and expense quantities used in the numerator of the ratio are derived by multiplying the reported average asset (liability) balance by the reported average asset (liability) rate, divided by four to convert annual to quarterly rates.

The model is specified according to the following equation:

**Equation A52** - Net Interest Income on Trading Assets and Liabilities Regression Model

$$Ratio(b,t) = \beta Treasury3m(t) + \alpha_b + \varepsilon(b,t)$$

*where:*

- $Treasury3m(t)$ is the 3-month Treasury yield, representing the risk-free short-term rate;

<!-- page 226 -->

- $\alpha_b$ represents firm-level fixed effects, which account for heterogeneity in the average level of the ratio over time across firms; and
- $\varepsilon(b,t)$ is the error term of the regression.

The data sample used for model estimation is an unbalanced panel of all FR Y-14Q reporters. The model is estimated as a weighted least squares (WLS) regression, weighted by the net trading asset balance (trading assets minus trading liabilities) in each firm-quarter. The Board selected a weighted panel regression to strike an appropriate balance between capturing data on all firms and avoiding undue influence from firm-quarters with very small trading positions that may generate volatile ratios.

<!-- Source PDF page 226 -->

<a id="sec-217"></a>

##### (b) Variable Selection

The Board examined three macroeconomic factors that could be plausibly related to net interest income on trading positions: the 3-month Treasury yield, the term spread (10-year minus 3-month Treasury yields), and the BBB corporate credit spread (BBB corporate bond yield minus 10-year Treasury yield). These variables could reflect interest income and expense streams arising from exposure to, respectively, short-term interest rates, long-term interest rates, and credit spreads.

The coefficient estimate on the 3-month Treasury yield was consistently positive and statistically significant, whether included in the model on its own or with any combination of the other two factors. However, the signs and statistical significance of the coefficient estimates on the other two factors varied depending on which other factors were included in the regression. This fact pattern is likely explained by the high correlations between the three macroeconomic factors over the sample period of the model. When short-term interest rates are low, the term spread and the credit spread both tend to be high; thus, it is difficult for the model to identify the
<!-- page 227 -->

effects of each factor separately. Furthermore, adding the two spread variables to the model with the 3-month Treasury yield did little to increase the overall explanatory power of the model. Therefore, in the interest of simplicity and model stability, the Board elected to include only the 3-month Treasury yield as an explanatory variable in the model.

Firms have individual preferences for holding trading assets, which can vary in risk, origination date, underlying interest rate terms (e.g., fixed vs. variable), and duration. Consequently, average yields vary across firms, even after controlling for macroeconomic factors. The regression model includes firm-specific fixed effects to account for this fact.

<!-- Source PDF page 227 -->

<a id="sec-218"></a>

##### (c) Assumptions and Limitations

The proposed model for this ratio is top-down in nature and does not attempt to capture the specific composition of any firm’s trading portfolio at any given point in time. Such compositional details could affect both the level of net interest income on trading positions at a given firm and its sensitivity to macroeconomic factors. As an example, firms with higher proportions of equity trading activity might have lower sensitivity to short-term interest rates, since equity positions do not generate interest income.

While differences in net interest income level are captured through the firm-specific fixed effects, differences in sensitivities are not. The Board considered including such compositional details in the model by, for example, incorporating information on trading asset and liability composition from the FR Y-9C, Schedules HC-D and HC-L or information on risk factor sensitivities from the FR Y-14Q, Schedule F. These additional data sources, however, would themselves be subject to significant limitations. The compositional information on the FR Y-9C, for example, focuses primarily on exposures to different types of cash securities, but has limited information on derivatives, which can have a significant impact on net interest income dynamics.
<!-- page 228 -->

The information on the FR Y-14Q, Schedule F, while more detailed, is only available for the subset of firms filing that schedule, meaning that a separate model would be needed for non-filers.

The Board assessed that using firm-specific fixed effects struck an appropriate balance of capturing cross-sectional variation in position profiles while retaining simplicity. In addition, the Board tested the assumption that sensitivity to the 3-month Treasury yield is constant across firms by running firm-specific regressions for all large trading firms using the same specification. In general, the coefficient estimates for the individual firms fell within the 95% confidence interval of the estimate from the weighted panel regression, supporting the use of a single common sensitivity estimate.

The model is estimated over a relatively long time period; thus, an implied assumption is that the spread and interest rate sensitivity of net interest income on trading positions for a given firm is stable over time. This assumption could conflict with the observation that firms may adjust their trading positions depending on macroeconomic conditions and other factors. The Board considered rolling-window firm-specific fixed effects as a possible alternative to full-sample fixed effects, which might help to capture changes over time in such firm preferences. However, introducing rolling-window fixed effects would also decrease the model’s stability and increase the volatility of projections, so the Board elected not to include rolling-window fixed effects.

Similarly, the Board assessed whether average sensitivity to macroeconomic factors across firms might vary over time by running rolling-window regressions and comparing coefficient estimates. This analysis suggested that the sensitivity to the 3-month Treasury rate may have increased over the most recent interest rate cycle compared to prior cycles. However,
<!-- page 229 -->

the Board decided that the full-sample sensitivity estimate was preferable to an estimate over a shorter recent period or using a model that weighed recent periods more heavily. Such approaches that assign higher importance to more recent periods could potentially result in less stable coefficient estimates and correspondingly higher volatility of projections.

Finally, as discussed above, the model has difficulty identifying separate effects from the term spread and credit spread factors due to high empirical correlations with the 3-month Treasury yield in the estimation data sample. This could result in a limitation where the model fails to capture sensitivity to these factors. One potential way of mitigating this limitation would be to use a data source with a longer time sample available, such as the FR Y-9C. However, this alternative data source has its own limitations, such as the fact that interest expense on trading liabilities is combined with interest expense on other borrowed money, and the correlations between the macroeconomic factors are likely to remain high even over longer samples. The Board believes that the potential concern is mitigated by the fact that firms with large trading operations are conceptually likely to limit the sensitivity of their net interest income on trading positions to long-term interest rates and credit spreads. This is because sensitivity of interest income implies sensitivity of market value, which large trading firms typically try to limit.

<!-- Source PDF page 229 -->

<a id="sec-219"></a>

##### (d) Questions

The Board is requesting public input on this proposed regression model for interest income and expense on trading assets and liabilities, including, but not limited to, input on the following questions:

*Question A188: The Board seeks comment on the proposed approach to model interest income and expense on trading assets and liabilities, as compared to the Board's current panel regression model.*
<!-- page 230 -->

<!-- Source PDF page 230 -->

<a id="sec-220"></a>

#### (2) Interest Expense on Other Borrowing

Interest expense on other borrowing, which includes interest expense paid on short-term borrowing, subordinated debt, and all other interest-bearing liabilities is modeled as a single quantity. The relevant balances for this component are the liabilities reported in line item 44C (Other Short-Term Borrowing), line item 46 (Subordinated Notes Payable to Unconsolidated Trusts Issuing TruPS and TruPS Issued by Consolidated Special Purpose Entities) and line item 47 (Other Interest-Bearing Liabilities) of the Net Interest Income Worksheet of FR Y-14Q, Schedule G. Parts of subordinated debt, however, may also be reported in line items 44C and 47 per reporting instructions. The Board selected the approach to model expenses on these liabilities together due to the relative simplicity of the approach, and due to lack of further granularity to cleanly separate subordinated debt from other borrowing from line items 44C and 47. The combined liabilities include subordinated debt, short-term borrowing such as commercial paper, advances from Federal Home Loan Bank, and other mid- to long-term debt.

<!-- Source PDF page 230 -->

<a id="sec-221"></a>

##### (a) Model Description

Under this modeling approach, the rate that each firm pays on its other borrowing depends on the contemporaneous level of the BBB corporate bond yield, the compositional mix of each firm’s portfolio, and a fixed effect estimated for each firm. More formally,

**Equation A53** - Interest Expense on Other Borrowing Regression Model

**A53(1):**

$$Expense(b,t) = R(b,t) \times B(b,t) = \left(Treasury3m(t) + \delta(b,t)\right) \times B(b,t)$$

with:

**A53(2):**

$$\delta(b,t) = \beta_1 BBB(t) + \beta_2 Commercial\ Paper(b,t) + \beta_3 Subdebt(b,t) + \alpha_b + \varepsilon(b,t)$$

<!-- page 231 -->

*where:*

- *Expense(b,t)* is the expense on Other Borrowing for each firm *b* at time *t*;
- *B(b,t)* is the total balance of other borrowing defined as the sum of other short-term, borrowing, subordinated debt, and other interest-bearing liabilities;
- *R(b,t)* represents the rate paid on other borrowings;
- $Treasury3m(t)$ is the 3-month Treasury rate at time| *t*;
- $\delta(b,t)$ is the firm-specific credit spread;|

- $BBB(t)$ is the BBB corporate bond yield at time $t$;
- $Commercial\ Paper(b,t)$ is the share of commercial paper relative to other borrowings for each firm $b$ at time $t$, calculated as the balance of commercial paper divided by the total balance of other borrowing;
- $Subdebt(b,t)$ is the share of subordinated debt relative to other borrowings for each firm $b$ at time $t$, calculated as the balance of subordinated debt divided by the total balance of other borrowing;
- $\alpha_b$ is the firm fixed effect for firm $b$; and
- $\varepsilon(b,t)$ is the error term in the regression.

The data sample used for model estimation is an unbalanced panel of all FR Y-14Q reporters from 2020:Q2 to 2021:Q4. The Board chose to restrict the sample to the specified time period so that the sensitivity to the economic and firm-specific factors, including the portfolio composition, is more precisely calibrated to a period where the interest rates are low.

The coefficients in the regression specified in equation A53(2) are estimated using ordinary least squares and are applied to each firm’s portfolio composition that is held constant at the lift-off quarter, as well as the scenario variable for the BBB corporate bond yield. Hence, for each projection quarter *q,* the firm’s interest expense is given by:

$$Expense(b,q) = \left(Treasury3m(q) + \delta(b,q)\right) \times B(b,0),$$

where the lift-off quarter is denoted by $q = 0$, and

$$\delta(b,q) = \beta_1 BBB(q) + \beta_2 Commercial\ Paper(b,0) + \beta_3 Subdebt(b,0) + \alpha_b.$$

##### (a.) Variable Selection

The Board examined three macroeconomic factors that could be plausibly related to interest expense on other borrowing: the 5- and 10-year U.S. Treasury rate and the BBB
<!-- page 232 -->

corporate bond yield. These variables could reflect interest expense streams arising from exposure to, respectively, short-term interest rates, long-term interest rates, and the overall credit conditions.

The coefficient estimate on the BBB corporate bond yield was consistently positive and statistically significant, whether included in the model on its own or with any combination of the other two factors. However, the statistical significance of the coefficient estimates on the other two factors varied depending on which other factors were included in the regression. This fact pattern is likely explained by the high correlations between the three macroeconomic factors over the sample period of the model.

The Board also considered the balance sheet composition variables for the firms’ liabilities. These variables are sourced from the FR Y-9C report. The balances on subordinated debt are reported in BHDM4062 and BHDMC699 in the FR Y-9C. The balances on commercial paper are reported in BHCK2309. The coefficients on these portfolio composition variables have the intuitive sign: since subordinated debt is more expensive, its coefficient is positive and statistically significant. Similarly, since commercial paper has a shorter time duration and is therefore more responsive to short-term interest rates (besides being usually highly rated with lower credit risk), its coefficient is negative and economically significant.

The mix of other borrowing, as well as interest rate risk hedging intensity, varies across firms, and this variation is not fully captured by the available portfolio composition variables. Consequently, average rates vary across firms, and the proposed regression model includes firm-specific fixed effects to account for this heterogeneity.
<!-- page 233 -->

<!-- Source PDF page 233 -->

<a id="sec-222"></a>

##### (b) Assumptions and Limitations

The model for this component does not fully capture the composition of each firm’s other borrowing beyond short-term commercial paper and subordinated debt. Such compositional details could affect both the level and sensitivity of the rate that each firm pays on its other borrowing. As an example, firms with a higher share of floating rate debt would have a higher sensitivity to changes in interest rates. Conversely, fully collateralized debt would be expected to have a lower rate due to its lower risk profile. This approach also does not account for the existing duration and maturity structure of various portions of each firm’s liabilities balances.

Additionally, the model is estimated over a specific time period when interest rates are low, assuming that the composition of other borrowing and the impact of interest rate risk hedges are similar during low interest rate periods, and the sensitivity of this component to credit conditions stays stable over other low interest rate periods. These assumptions may conflict with the observation that the firms may adjust their borrowing sources and hedging strategies over time, depending on the availability of alternative funding sources, such as deposits, as well as macroeconomic and overall credit conditions.

<!-- Source PDF page 233 -->

<a id="sec-223"></a>

##### (c) Questions

*Question A189: The Board is requesting public input on this proposed approach to modeling interest expense on other borrowing. What are the advantages or disadvantages of using this proposed approach?*

*Question A190: The Board proposes modeling interest expense on subordinated debt jointly with other components of other borrowing. What are the advantages and disadvantages*
<!-- page 234 -->

*of this approach? Should the Board continue to model interest expense on subordinated debt separately?*

*Question A191: The Board incorporates other borrowing portfolio composition differences by using shares of commercial paper and subordinated debt. Are there other approaches that the Board should consider?*

<!-- Source PDF page 234 -->

<a id="sec-224"></a>

### e. Estimated Parameters for Proposed Regression Models

As described in the last subsections, there are two components of pre-provision net revenue that are based on regression models as part of the proposed models for the 2026 stress test: (1) net interest income on trading assets and liabilities, and (2) interest expense on other borrowing. Table A9 presents the estimated coefficients for these two models. Included in the table are the independent macroeconomic variables estimated coefficients for each model. Estimated coefficients for firm fixed-effects are not included in the table. The Board calculated these coefficients based on data submitted on forms FR Y-14Q and FR Y-9C.

**Table A9** - Estimated Parameters for Proposed Regression Models

| Component (Relevant Equation) | 3M Treasury yield | BBB corporate bond yield | Share of commercial paper relative to other borrowing | Share of subordinated debt relative to other borrowing | Firm fixed-effects |
|---|---|---|---|---|---|
| Net interest income on trading assets and liabilities (Equation A52) | 0.278*** | | | | Yes |
| Interest expense on other borrowing (Equation A53(2)) | | 0.254** | -0.036*** | 0.066** | Yes |

Notes: Statistical significance levels of 1%, 5%, and 10% are indicated as ***, **, and *, respectively.

<!-- page 235 -->

<!-- Source PDF page 235 -->

<a id="sec-225"></a>

### f. Proposed Noninterest Income and Expense Models Using Firm Projections

The Board is proposing alternative model specifications to project noninterest income and noninterest expense components of pre-provision net revenue utilizing data reported in the FR Y-14A and FR Y-14Q schedules. These schedules include categories of noninterest income and noninterest expense that provide more detail than the more highly aggregated FR Y-9C schedule. The FR Y-14A data also contain firm projections for Category I – III banks for the supervisory baseline and severely adverse scenarios. Firm projections provide insights into which macroeconomic variables are the most relevant for different types of noninterest income and form the basis for the proposed noninterest income and expense models.

<!-- Source PDF page 235 -->

<a id="sec-226"></a>

#### (1) Noninterest Income

The Board proposes to utilize FR Y-14A and FR Y-14Q data to model noninterest income.

<!-- Source PDF page 235 -->

<a id="sec-227"></a>

##### (a) Model Specification

The Board proposes modeling noninterest income utilizing these additional schedules via the following six steps:

1. Use data reported in the FR Y-14A schedule to construct an aggregate industry-level time

series for ten components of noninterest income, where the aggregate includes available

data from the banks participating in the current exercise.

2. For each noninterest income component in each historical stress testing exercise,

calculate the discount factor path. The discount factor path represents the cumulative

percentage growth of the component relative to its average over the 12 quarters

immediately preceding that exercise.

3. Develop a simple regression model to express each discount factor path as a function of

variables from the supervisory severely adverse scenario of the corresponding historical

stress testing exercise.

4. Use the estimated regression to project the ten component-level discount factor paths

conditional on the supervisory severely adverse scenario of the current exercise. 5. To obtain a firm’s income for each component, multiply its trailing 12-quarter average

income for that component by the relevant discount factor path.
<!-- page 236 -->

6. Sum the ten component-level projections to obtain the projected path of noninterest

income for the firm.

<!-- Source PDF page 236 -->

<a id="sec-228"></a>

##### (b) Variable Selection

The Board proposes modeling the following ten components of noninterest income utilizing this approach and the data from FR Y-14Q and FR Y-14A schedules:

a. Deposit-related noninterest income (row 14O of FR Y-14Q, Schedule G and FR Y-14A,

Schedule A.7.a);

b. Credit and charge card loan-related noninterest income (row 14B of FR Y-14Q, Schedule

G and FR-Y-14A Schedule, A.7.a);

c. Other loan-related noninterest income (rows 14E, 14S, and 15 of FR Y-14Q, Schedule G

and FR Y-14A, Schedule A.7.a);

d. Sales & trading noninterest income (row 18 of FR Y-14Q, Schedule G and FR Y-14A,

Schedule A.7.a);

e. Investment banking and merchant banking/private equity noninterest income (rows 16

and 17 of FR Y-14Q, Schedule G and FR Y-14A, Schedule A.7.a);

f. Asset management noninterest income (row 19A of FR Y-14Q, Schedule G and FR Y-

14A, Schedule A.7.a);

g. Wealth management /private banking noninterest income (row 19B of FR Y-14Q,

Schedule G and FR Y-14A, Schedule A.7.a);

h. Investment services noninterest income (row 20 of FR Y-14Q, Schedule G and FR Y-

14A, Schedule A.7.a);

i. Treasury services noninterest income (row 21 of FR Y-14Q, Schedule G and FR Y-14A,

Schedule A.7.a); and

j. Miscellaneous noninterest income (rows 14T and 22 – 25 of FR Y-14Q, Schedule G and

FR Y-14A, Schedule A.7.a).

The Board considered the following factors in constructing the categories to measure noninterest income:

- Utilization of broad categories (asset management fees, investment banking fees, trading, etc.) that large banks themselves typically use in their communications with investors to

report noninterest income;

- Ability to control for revenue changes that result from balance sheet dynamics to ensure that projections are consistent with the Board’s constant balance sheet assumption where

necessary;

- Separation into categories that have distinct reactions to macroeconomic factors based on historical FR Y-14Q data and projection data from the FR Y-14A; and
- Avoiding categories in which most of the revenue is generated by a small number of firms.
<!-- page 237 -->

To control for fluctuations in noninterest income across firms due to balance sheet dynamics, the Board uses scaling balances for certain components. For example, loan-related noninterest income may fall in the projection period because firms are projecting lower balance amounts and not because they are cutting fees. To account for this and to make the projection path consistent with the assumption that firms maintain constant balance sheets over the projection horizon, the Board divides the revenue measure by an appropriate scaling balance. Scaling balances are obtained from the balance sheet portion of FR Y-14A or FR Y-9C. Four categories of noninterest income (NII) are assumed to require a scaling balance:

a. Deposit-related NII, which uses deposits as the scaling balance (row 134 of FR Y-14A,

Schedule A.1.b and row 13.a of FR Y-9C, Schedule HC);

b. Credit and charge card loan-related NII, which uses credit card loans as the scaling

balance (row 35 of FR Y-14A, Schedule A.1.b and row 6.a of FR Y-9C, Schedule HC); c. Other loan-related NII, which uses non-credit card loans as the scaling balance (row 31 of

FR Y-14A, Schedule A.1.b minus row 35 FR Y-14A, Schedule A.1.b and row 12 of FR Y-

9C, Schedule HC minus row 6.a. of FR Y-9C, Schedule HC);

d. Sales & trading NII, which uses trading assets as the scaling balance (row 112 of FR Y-

14A, Schedule A.1.b and row 5 of FR Y-9C, Schedule HC).

The remaining six categories are assumed to not require a scaling balance. None of the fluctuations in revenue that occur in the projection period are assumed to result from changing balances. It could be argued that assets under management (AUM) is a suitable scaling balance for asset management, wealth management, and investment servicing components. However, using AUM as a scaling balance would embed the assumption that AUM is constant over the projection horizon. This would be inconsistent with the decline in market indices that is a recurring feature of the supervisory severely adverse scenario.

The Board defines a discount factor for a given category of noninterest income as follows:
<!-- page 238 -->

**Equation A54** - Discount Factor Calculation for Noninterest Income Categories

$$DF(c)_t^E = \left[\, NII(c)_t^E / SB(c)_t^E \,\right] \, / \, \left[\, NII(c)_{Base}^E / SB(c)_{Base}^E \,\right]$$

*where:*

- $DF(c)_t^E$ is the discount factor for category $c$ in exercise $E$ in quarter $t$;
- $NII(c)_t^E$ is the industry-level noninterest income for category $c$ in exercise $E$ in quarter $t$;
- $SB(c)_t^E$ is the industry-level scaling balance for category $c$ in exercise $E$ in quarter $t$ (for categories with no scaling balance, $SB(c)_t^E$ equals one);[^67]
- $E$ is the stress testing exercise (from 2014 until the most recent exercise);
- $t$ is the projection quarter (PQ1 – PQ9);
- $NII(c)_{Base}^E$ is the average industry-level noninterest income for category $c$ across the trailing 12 historical quarters before PQ1 of exercise E; and
- $SB(c)_{Base}^E$ is the average industry-level scaling balance for category $c$ across the trailing 12 historical quarters before PQ1 of exercise $E$ (for categories with no scaling balance, $SB(c)_{Base}^E$ equals one).

In the above calculations, industry-level measures are the simple sums across all firms that have projections reported in FR Y-14A for a given stress testing exercise. Revenue and scaling balances in the base period are measured over a trailing 12-quarter period. The selection of 12 quarters satisfies competing considerations of reducing volatility in projections from one exercise to another and reflecting changes over time in the level and composition of a firm’s noninterest income.

The Board estimates a regression model for each component, where the dependent variable is the discount factor path for that component. Discount factors from multiple exercises and across all of the projection quarters are combined, and a single pooled ordinary least squares model is estimated with no exercise-specific fixed effects.

The independent variables are drawn from the severely adverse scenario and are differenced as appropriate to ensure stationarity. Differences are in general calculated with respect to PQ0 for consistency with the discount factor path, which is calculated on a cumulative basis. This approach is appropriate for most components where differencing is applied. For
<!-- page 239 -->

example, firms’ noninterest income from asset management is a function of assets under management and is thus expected to fluctuate with the cumulative change in the Dow Jones index. As indicated below, for sales and trading and investment banking, the Board proposes to apply a 1-quarter difference to the independent variable rather than a cumulative difference. For these businesses, the 1-quarter difference provides improved fit and greater explanatory power relative to the cumulative difference. Applying a 1-quarter difference is also consistent with the observation that revenues in these businesses may recover before market indices return to their previous levels.

The Board would plan to monitor the performance of the models and may update the estimation sample in future cycles to include additional years of firm projections. For example, for 2025 stress test projections, the sample includes firm projections from 2014 to 2024, excluding 2025 projections. The Board applies pro forma treatment to FR Y-14Q only in years when the firm’s projections reflect the merged entity.

For modeling deposit-related noninterest income the Board uses the following specification:

**Equation A55** – Deposit-related Noninterest Income Discount Factor

$$DF(E,t) = \beta_0 + \beta_1 Q_1 + \beta_2 Q_2 + \beta_3 Q_3 + \beta_4 Q_4 + \beta_5 Q_5 + \beta_6 Q_6 + \beta_7 Q_7 + \beta_8 Q_8 + \varepsilon(E,t)$$

*where:*

- $DF(E,t)$ is the industry-level discount factor from exercise $E$ in projection quarter $t$;
- $\beta_0$ is the constant term estimated by the regression;
- $Q_1$ is an indicator variable equal to 1 in projection quarter 1 and 0 in all other quarters;
- $Q_2$ is an indicator variable equal to 1 in projection quarter 2 and 0 in all other quarters;
- $Q_3$ is an indicator variable equal to 1 in projection quarter 3 and 0 in all other quarters;
- $Q_4$ is an indicator variable equal to 1 in projection quarter 4 and 0 in all other quarters;
- $Q_5$ is an indicator variable equal to 1 in projection quarter 5 and 0 in all other quarters;
- $Q_6$ is an indicator variable equal to 1 in projection quarter 6 and 0 in all other quarters;

<!-- page 240 -->

- $Q_7$ is an indicator variable equal to 1 in projection quarter 7 and 0 in all other quarters;
- $Q_8$ is an indicator variable equal to 1 in projection quarter 8 and 0 in all other quarters; and
- $\varepsilon(E,t)$ is the error term of the regression.

For modeling credit and charge card loan-related noninterest income the Board uses the following specification:

**Equation A56** – Credit and Charge Card Loan-related Noninterest Income Discount Factor

$$DF(E,t) = \beta_0 + \beta_1 URQ(E,t) + \varepsilon(E,t)$$

*where:*

- $DF(E,t)$ is the industry-level discount factor from exercise $E$ in projection quarter $t$;
- $\beta_0$ is the constant term estimated by the regression;
- $URQ(E,t)$ is the quarterly change in the unemployment rate in exercise $E$ at projection quarter $t$, representing changes in aggregate economic conditions; and
- $\varepsilon(E,t)$ is the error term of the regression.

For modeling other loan-related noninterest income the Board uses the following specification:

**Equation A57** – Other Loan-related Noninterest Income Discount Factor

$$DF(E,t) = \beta_0 + \beta_1 URQ(E,t) + \varepsilon(E,t)$$

*where:*

- $DF(E,t)$ is the industry-level discount factor from exercise $E$ in projection quarter $t$;
- $\beta_0$ is the constant term estimated by the regression;
- $URQ(E,t)$ is the quarterly change in the unemployment rate in exercise $E$ at projection quarter $t$, representing changes in aggregate economic conditions; and
- $\varepsilon(E,t)$ is the error term of the regression.

For modeling sales and trading related noninterest income the Board uses the following specification:

**Equation A58** - Sales and Trading Noninterest Income Discount Factor

$$DF(E,t) = \beta_0 + \beta_1 DJQ(E,t) + \varepsilon(E,t)$$

*where:*

- $DF(E,t)$ is the industry-level discount factor from exercise $E$ in projection quarter $t$;
- $\beta_0$ is the constant term estimated by the regression;
- $DJQ(E,t)$ is the quarterly change in the Dow Jones Total Stock Market Index in exercise $E$ at projection quarter $t$, representing changes in equity market conditions; and

<!-- page 241 -->

- $\varepsilon(E,t)$ is the error term of the regression.

For modeling noninterest income from investment banking and merchant banking/private equity, the Board proposes using the following specification:

**Equation A59** - Investment Banking and Merchant Banking / Private Equity Noninterest Income Discount Factor|

$$DF(E,t) = \beta_0 + \beta_1 DJQ(E,t) + \beta_2 BBBSpread(E,t) + \varepsilon(E,t)$$

*where:*

- $DF(E,t)$ is the industry-level discount factor from exercise $E$ in projection quarter $t$;
- $\beta_0$ is the constant term estimated by the regression;
- $DJQ(E,t)$ is the quarterly change in the Dow Jones Total Stock Market Index in exercise $E$ at projection quarter $t$, representing changes in equity market conditions;
- $BBBSpread(E,t)$ is the spread of the BBB Bond Index Yield to the 10-year Treasury Yield in exercise $E$ at projection quarter $t$, representing revaluation adjustments due to changes in the risk premium; and
- $\varepsilon(E,t)$ is the error term of the regression.

For modeling noninterest income from asset management, the Board uses the following specification:

**Equation A60** - Asset Management Noninterest Income Discount Factor

$$DF(E,t) = \beta_0 + \beta_1 DJC(E,t) + \varepsilon(E,t)$$

*where:*

- $DF(E,t)$ is the industry-level discount factor from exercise $E$ in projection quarter $t$;
- $\beta_0$ is the constant term estimated by the regression;
- $DJC(E,t)$ is the cumulative change in the Dow Jones Total Stock Market Index in exercise $E$ from Q0 to projection quarter $t$, representing changes in equity market conditions; and
- $\varepsilon(E,t)$ is the error term of the regression.

For modeling noninterest income from wealth management, the Board uses the following specification:

**Equation A61** - Wealth Management Noninterest Income Discount Factor

$$DF(E,t) = \beta_0 + \beta_1 DJC(E,t) + \beta_2 RGDP(E,t) + \varepsilon(E,t)$$

<!-- page 242 -->

*where:*

- $DF(E,t)$ is the industry-level discount factor from exercise $E$ in projection quarter $t$;
- $\beta_0$ is the constant term estimated by the regression;
- $DJC(E,t)$ is the cumulative change in the Dow Jones Total Stock Market Index in exercise $E$ from Q0 to projection quarter $t$, representing changes in equity market conditions;
- $RGDP(E,t)$ is the cumulative change in real GDP in exercise $E$ from Q0 to projection quarter $t$, representing changes in the overall macroeconomic environment; and
- $\varepsilon(E,t)$ is the error term of the regression.

For modeling noninterest income from investment services, the Board proposes using the following model:

**Equation A62** - Investment Services Noninterest Income Discount Factor

$$DF(E,t) = \beta_0 + \beta_1 RGDP(E,t) + \beta_2 BBBSpread(E,t) + \varepsilon(E,t)$$

*where:*

- $DF(E,t)$ is the industry-level discount factor from exercise $E$ in projection quarter $t$;
- $\beta_0$ is the constant term estimated by the regression;
- $RGDP(E,t)$ is the cumulative change in real GDP in exercise $E$ from Q0 to projection quarter $t$, representing changes in the overall macroeconomic environment;
- $BBBSpread(E,t)$ is the spread of the BBB Bond Index Yield to the 10-year Treasury Yield in exercise $E$ at projection quarter $t$, representing revaluation adjustments due to changes in the risk premium; and
- $\varepsilon(E,t)$ is the error term of the regression.

For modeling noninterest income from treasury services, the Board proposes using the following model:

**Equation A63** - Treasury Services Noninterest Income Discount Factor

$$DF(E,t) = \beta_0 + \beta_1 Q_1 + \beta_2 Q_2 + \beta_3 Q_3 + \beta_4 Q_4 + \beta_5 Q_5 + \beta_6 Q_6 + \beta_7 Q_7 + \beta_8 Q_8 + \varepsilon(E,t)$$

*where:*

- $DF(E,t)$ is the industry-level discount factor from exercise $E$ in projection quarter $t$;
- $\beta_0$ is the constant term estimated by the regression;
- $Q_1$ is an indicator variable equal to 1 in projection quarter 1 and 0 in all other quarters;
- $Q_2$ is an indicator variable equal to 1 in projection quarter 2 and 0 in all other quarters;
- $Q_3$ is an indicator variable equal to 1 in projection quarter 3 and 0 in all other quarters;
- $Q_4$ is an indicator variable equal to 1 in projection quarter 4 and 0 in all other quarters;
- $Q_5$ is an indicator variable equal to 1 in projection quarter 5 and 0 in all other quarters;

<!-- page 243 -->

- $Q_6$ is an indicator variable equal to 1 in projection quarter 6 and 0 in all other quarters;
- $Q_7$ is an indicator variable equal to 1 in projection quarter 7 and 0 in all other quarters;
- $Q_8$ is an indicator variable equal to 1 in projection quarter 8 and 0 in all other quarters; and
- $\varepsilon(E,t)$ is the error term of the regression.

Finally, the Board proposes to model miscellaneous noninterest income using the following specification:

**Equation A64** - Miscellaneous Noninterest Income Discount Factor

$$DF(E,t) = \beta_0 + \beta_1 URQ(E,t) + \beta_2 Treasury10y(E,t) + \varepsilon(E,t)$$

*where:*

- $DF(E,t)$ is the industry-level discount factor from exercise $E$ in projection quarter $t$;
- $\beta_0$ is the constant term estimated by the regression;
- $URQ(E,t)$ is the quarterly change in the unemployment rate in exercise $E$ at projection quarter $t$, representing changes in aggregate economic conditions;
- *Treasury10y* is the quarterly change in the 10-year Treasury yield in exercise $E$ at projection quarter $t$, representing changes in the level of interest rates; and
- $\varepsilon(E,t)$ is the error term of the regression.

To obtain a firm’s noninterest income projection for each component, the Board multiplies the trailing 12-quarter average income for the component by the relevant discount factor path. The Board obtains the projected path of noninterest income for the firm by adding the ten component paths.

The Board designed these models to be simple and include macroeconomic variables that have stable and intuitive relationships with the underlying noninterest income components.

<!-- Source PDF page 243 -->

<a id="sec-229"></a>

##### (c) Assumptions and Limitations

The Board made several assumptions when considering the alternative approach to modeling noninterest income as described above.

The FR Y-14 schedules identify 12 summary categories of noninterest income, many of which are sub-divided into smaller components. The modeling approach described herein could
<!-- page 244 -->

be undertaken using the full set of granular components. The Board chose to use ten high-level aggregates for simplicity and tractability.

When constructing the discount factors the Board followed the simplest approach: adding total revenue across the firms and then dividing that amount by the sum of the scaling balance. This is equivalent to constructing a weighted average, where the scaling balances are used to determine the weights. An alternative approach would be to derive weights from the revenue amounts. It is also possible to construct individual firm-level discount factors and then calculate the weighted median.

The Board made certain assumptions on how to compute the base value of the discount factor. The Board found that the trailing 12-quarter period balances competing considerations of reducing volatility in projections from one exercise to another, while also reflecting recent changes in the level and composition of a firm’s noninterest income. However, a different weighting of these competing considerations could support a different lookback period for computing the base value.

In certain limited instances within the miscellaneous noninterest income component, a firm’s trailing 12-quarter average income is negative. Given the structure of the model, this implies that the PQ1 projection for that firm’s miscellaneous noninterest income will also be negative, and that the projection path will tend to increase from PQ1 to PQ9.

The Board selected macroeconomic variables that have the highest explanatory power and correlations with the corresponding components of noninterest income. However, other variables or approaches might also be possible.
<!-- page 245 -->

When constructing the discount factors, the Board chose to use data beginning in 2014 and to focus on severely adverse scenario projections. The Board could consider using baseline projections to further inform these models of noninterest income.

<!-- Source PDF page 245 -->

<a id="sec-230"></a>

##### (d) Questions

The Board is requesting public input on this proposed set of models for noninterest income based on firms’ projections from the FR Y-14A, including, but not limited to, input on the following questions:

*Question A192: The Board seeks comment on the proposed approach to model noninterest income based on firms’ projections reported on form FR Y-14A, as compared to the Board's current panel regression model.*

*Question A193: The Board is proposing to use historical projections beginning in 2014. What are the advantages and disadvantages of this choice? Should the Board consider a shorter series?*

*Question A194: The Board is proposing to model noninterest income using separate regression models for each of ten noninterest income components. Should the Board consider an alternative set of noninterest income components to better capture each firm’s business model?*

*Question A195: Category IV firms are not required to provide projections. If the Board were to implement the proposed alternative framework to modeling noninterest income, should it also collect projections from Category IV firms? What would be advantages and disadvantages of doing so? Should the Board consider including Category IV firms in the estimation data in years in which they submitted firm projections via FR Y-14A (prior to 2018)?*
<!-- page 246 -->

*Question A196: The Board is proposing to use firm projections from the supervisory severely adverse scenario. Should the Board consider also using firm projections from the baseline scenario?*

*Question A197: The final projected discount factor that results from combining the regression coefficients with the new scenario data is applied as a cumulative growth rate. When the growth rate is negative and the starting base revenue amount is positive, the projected revenue amount declines (as expected). However, if the starting revenue amount is negative, the projected revenue amount increases as it approaches zero. Is there a different assumption that the Board should consider when modeling the final projected discount factor? What are the advantages and disadvantages of using this approach?*

<!-- Source PDF page 246 -->

<a id="sec-231"></a>

#### (2) Noninterest Expense Model Using the Efficiency Ratio Projections

The Board proposes an alternative approach to model noninterest expense that is based on the concept of an efficiency ratio. The efficiency ratio is a measure commonly used by financial firms that quantifies how effectively a bank converts revenue into profit by comparing total operating expenses to total revenue.

The proposed model integrates firm-submitted projections with Board internal projections to produce projections of total noninterest expense, excluding operational risk. Currently, individual components of noninterest expense, such as compensation, fixed assets, and all other expenses are modeled separately. While the current approach offers flexibility in modeling individual expense components, historical experience, as well as firm projections, suggests that expenses and revenues tend to move together, which may not always occur in the current approach.
<!-- page 247 -->

<!-- Source PDF page 247 -->

<a id="sec-232"></a>

##### (a) Model Description

The proposed model replaces individual models for compensation, fixed assets, and all other noninterest expenses with a unified approach that treats total noninterest expense as a single component, using the concept of an efficiency ratio (ER). The efficiency ratio measures how effectively a bank converts revenue into profit by comparing operation expenses to revenue. By leveraging variation in revenue composition across business lines, this approach captures differences in firm business models, while ensuring that projected expenses are more closely aligned with projected revenues.

The efficiency ratio, expressed as a percentage, is calculated as follows:

**Equation A65 -** Efficiency Ratio Calculation

$$\text{Efficiency Ratio} = \frac{\text{Total Noninterest Expense} - \text{Operational Risk}}{\text{Net Interest Income} + \text{Noninterest Income}} * 100$$

A lower efficiency ratio indicates higher efficiency, meaning the bank is spending less to generate each dollar of revenue. Although this ratio typically includes operational risk losses when used by the financial industry, the Board excludes these losses in this model as they are already modeled separately, and due to their unique characteristics under stress.

The linear model[^68] is specified as follows:

**Equation A66** - Efficiency Ratio Projection

<!-- page 248 -->

trend in ER over time. A positive coefficient implies ER is increasing over projection quarters, while a negative $\beta$ suggests improving efficiency. The $\gamma_j$ coefficients capture the effect of different business segment revenue shares on ER. The term $\epsilon_{i,t}^{ST}$ represents the error term in the regression. To calculate revenue shares, we use the following equation:

**Equation A67** – Revenue Shares Calculation

$$\frac{Revenue_j}{TotalRevenue} = \frac{\text{Total revenue from component j for the past 5 years}}{\text{Total revenue across all components for the past 5 years}} * 100$$

The revenue share varies across banks, stress test years, and revenue streams. This specification implies that all banks share the same sensitivity to both quarter and the various revenue streams.

The Board uses eleven revenue shares representing different business lines: one for net interest income and ten for noninterest income, consistent with the proposed noninterest income models. Noninterest income is further disaggregated into the categories: credit card loans, non-credit card loans, deposit-related, sales and trading, investment banking and merchant banking, asset management, wealth management and private banking, asset servicing, treasury, and miscellaneous categories.

To calculate revenue shares at the jump-off quarter for each stress test year, the Board defines a 5-year lookback window. As one of the goals of this expense model is to stabilize PPNR, this relatively longer window will reduce year-over-year volatility in ERs. When revenue composition is stable over time, the predicted ERs, and thus expenses, will also tend to be more stable. In terms of data, the Board relies on firm projections submitted through FR Y-14A and calculates revenue shares based on historical data from FR Y-14Q. The Board would plan to monitor the performance of the models and may update the estimation sample in future cycles to
<!-- page 249 -->

include additional years of firm projections. For example, in the 2025 stress test, the sample includes projections from 2015 to 2024, excluding 2025 projections. Observations with negative ER projections are excluded and firms that are still in the 2025 stress testing cycle are retained in the sample. The bank sample includes both disclosed and nondisclosed banks but excludes new entrants. Prior to 2018, the sample includes projections from firms in Category I through IV (as defined in 2025 stress test) that submitted data. Beginning in 2018, the sample is limited to projections from firms in Category I through III due to regulatory changes. Consistent with existing pre-provision net revenue treatment, we exclude other real estate owned (OREO), off-balance-sheet credit exposure, and provisions for the mortgage repurchase reserve. The Board applies pro forma treatment to FR Y-14Q only in years when the firm’s projections reflect the merged entity. This adjustment ensures that, when evaluating firm projections, we do not treat a firm as if it was already merged at the time of projection. Once the model is estimated, the Board generates firm-specific ER paths, including for Category IV firms. ER paths are estimated using this model only for quarters 1 through 9; beyond quarter 9, ER paths are assumed to remain flat. These projected paths are then combined with projected total revenues from the supervisory models to compute noninterest expense using the following formula, with a minimal floor of zero:

**Equation A68** - Noninterest Expense Projection

$$\widehat{NIE_{i,t}} = max\left(0, \widehat{ER_{i,t}} * Total\widehat{Revenue}_{i,t}\right)$$

<a id="sec-233"></a>

##### (b) Assumptions and Limitations

This approach offers several advantages. First, it is simple and concise, reducing the number of estimated parameters while still capturing key revenue drivers of efficiency ratios. Unlike the current approach, which models individual noninterest expense components
<!-- page 250 -->

separately and does not incorporate revenues, this model directly links total noninterest expense to total revenue. By integrating firm-submitted projections, it leverages forward-looking information about how banks expect to operate under the severely adverse scenario. However, there are several limitations to this approach. Although the model adopts the same revenue breakdowns, this categorization may not be optimal for capturing firm-level heterogeneity in efficiency ratios. Additionally, while the model allows for firm-specific ER paths, it assumes they are parallel across firms. Allowing more flexible functional forms could improve projections by capturing different ER dynamics across banks. For example, the model could include multiple interaction terms between quarter and revenue shares, enabling each firm to exhibit a distinct ER path, depending on its compositions of revenues. Another limitation is that the model is calibrated using information only from firms that submit projections; in particular, following 2018 Category IV firms are excluded from the estimation sample. Regarding data treatment, in transitioning to FR Y-14 data, a new process to identify unusual items - as is currently done with FR Y-9C data- will need to be developed; this may be more challenging for the FR Y-14A projections.

<!-- Source PDF page 250 -->

<a id="sec-234"></a>

##### (c) Questions

The Board is requesting public input on this proposed set of models for noninterest expense using efficiency ratios, including, but not limited to, input on the following questions:

*Question A198: The Board seeks comment on the proposed approach to model noninterest expense based on the efficiency ratios, as compared to the Board's current panel regression model.*
<!-- page 251 -->

*Question A199: Is an approach tying noninterest expenses to revenues through efficiency ratios preferable to the current approach in which expenses are modeled independently? What are the advantages and disadvantages of this approach?*

*Question A200: Does the specification sufficiently capture cross-firm differences? For example, would different revenue and expense categories be preferable? Would a more flexible functional form be preferable to the proposed simple linear model? Should a shorter time window be used to compute the firm revenue mix? Does the specification adequately capture outlier firms with highly concentrated revenues?*

*Question A201: What are the advantages and disadvantages of using firm projections to calibrate the efficiency ratios versus an approach based on historical data?*

*Question A202: Is the proposed approach sufficient to also model efficiency ratios for Category IV firms that do not submit FR Y-14A projections?*

<!-- Source PDF page 251 -->

<a id="sec-235"></a>

### g. Estimated Parameters for Proposed Noninterest Income and Expense Models Using Firm Projections

The tables included in this section present the estimated parameters (coefficients) for all models of noninterest income and expense proposed for the 2026 stress test. Table A10 presents the estimated coefficients for all the regressions that are part of the proposed discount factor models. Included in the table are, for each model, the estimated coefficients for the intercept, for the independent macroeconomic variables, and for the seasonal dummies (when included in the specification).
<!-- page 252 -->

Table A11 presents the estimated coefficients for the proposed efficiency ratio path regression. Included in this table are the estimated coefficients for the intercept, the time trend, and the revenue shares.
<!-- page 253 -->

**Table A10** - Estimated Parameters for Proposed Noninterest Income Discount Factor Models

| Discount Factor (Relevant Equation) | Intercept | Quarterly change in the unemployment rate[^69] | Quarterly Change in the Dow Jones Total Stock Market Index[^70] | Spread of the BBB bond index yield to the 10-year Treasury yield | Cumulative change in the Dow Jones Total Stock Market Index[^71] | Cumulative change in Real GDP[^72] | Quarterly change in the 10-year Treasury yield[^73] | Projection quarter indicators |
|---|---|---|---|---|---|---|---|---|
| Deposit-related (Equation A55) | 0.719*** | | | | | | | q_2 = 0.008; q_3 = 0.023; q_4 = 0.012; q_5 = -0.023; q_6 = -0.009; q_7 = 0.005; q_8 = -0.005; q_9 = -0.044 |
| Credit and charge card loan-related (Equation A56) | 0.950*** | -0.071*** | | | | | | |
| Other loan-related (Equation A57) | 0.734*** | -0.128*** | | | | | | |
| Sales and trading (Equation A58) | 0.908*** | | 1.748*** | | | | | |
| Investment banking and merchant banking/private equity (Equation A59) | 0.828*** | | 1.810*** | -0.081*** | | | | |
| Asset management (Equation A60) | 0.938*** | | | | 0.605*** | | | |
| Wealth management (Equation A61) | -1.699*** | | | | 0.492*** | 2.842*** | | |
| Investment services (Equation A62) | -0.266* | | | -0.030*** | | 1.328*** | | |
| Treasury services (Equation A63) | 1.028*** | | | | | | | q_2 = 0.003; q_3 = -0.008; q_4 = -0.036**; q_5 = -0.051***; q_6 = -0.038**; q_7 = -0.032**; q_8 = -0.032**; q_9 = -0.027* |
| Miscellaneous (Equation A64) | 0.735*** | -0.245*** | | | | | 0.208*** | |

Notes: Statistical significance levels of 1%, 5%, and 10% are indicated as ***, **, and *, respectively.

<!-- page 254 -->

Notes: Statistical significance levels of 1%, 5%, and 10% are indicated as ***, **, and *, respectively.
<!-- page 255 -->

**Table A11** - Estimated Parameters for the Proposed Efficiency Ratio Model (Equation A66)

| Variable | Coefficient |
|---|---|
| Intercept | 126.967*** |
| Time trend | -0.923*** |
| Net interest income revenue share | -0.570*** |
| Credit card loans noninterest income revenue share | -1.374*** |
| Non-credit card loans noninterest income revenue share | -1.065*** |
| Deposit-related noninterest income revenue share | -0.928*** |
| Sales and trading noninterest income revenue share | -0.946*** |
| Investment banking and merchant banking noninterest income revenue share | 0.376** |
| Asset management noninterest income revenue share | -0.017 |
| Wealth management and private banking noninterest income revenue share | -0.166*** |
| Investment servicing noninterest income revenue share | -0.499*** |
| Treasury noninterest income revenue share | -0.312 |

Notes: Statistical significance levels of 1%, 5%, and 10% are indicated as ***, **, and *, respectively. The omitted category (base case) in this regression is “miscellaneous”.

---

## Footnotes

[^1]: Capital-neutral excluded revenue or expense components are: (i) goodwill impairment losses, (ii) provisions to repurchase reserve/liability for residential mortgage representations and warranties, (iii) valuation adjustment for the firm’s own debt under the fair value option, and (iv) impact of debt valuation adjustment of trading revenue changes on the firm’s derivative liabilities creditworthiness. Because projecting capital-neutral flows would not impact stress testing outcomes, the Board excludes these components from the pre-provision net revenue models. Excluded revenue or expense components that are projected by other model suites consist of: (i) net gains (losses) on sales of other real estate owned and (ii) operational risk expenses. These two components were judged by the Board to be sufficiently different in nature from the remaining pre-provision net revenue components to justify separate modeling approaches.

[^2]: In modeling pre-provision net revenue, the Board makes adjustments to eliminate or minimize potential double-counting of losses. For example, the Board adjusts historical data series to exclude losses from operational-risk events and other real estate owned expenses, which are modeled separately, as described in footnote 1. The Board also excludes expenses related to special assessments from the Federal Deposit Insurance Corporation, as well as certain non-recurring expenses, when modeling pre-provision net revenue. Non-recurring expenses - such as merger related expenses - are excluded from the stress testing exercise on the grounds that there is no expectation they would occur in the hypothetical scenario being tested.

[^3]: See Hirtle, B., Kovner, A., Vickery, J. and Bhanot, M., 2016. Assessing financial stability: The capital and loss assessment under stress scenarios (CLASS) model. Journal of Banking & Finance, 69, pp.S35-S55.

[^4]: While there is not much academic literature on modeling pre-provision net revenue, particularly under stressful economic conditions, the Board did incorporate findings from a few other studies when designing its own pre-provision net revenue models. For example, Stiroh (2004) finds a relatively weak relationship between business cycles and aggregate net interest income and noninterest income, although noninterest income appears to be more cyclical than net interest income. In another study, Albertazzi and Gambacorta (2009) estimated equations for net interest income, noninterest income, and operating expenses for an international sample of banks in industrialized countries, assessing the relationship between macroeconomic variables and bank profits. They find that most of the explanatory power arises from lagged values of the dependent variable rather than the regressors also alluding to persistence of bank profitability. See Stiroh, K.J., 2004. Diversification in banking: Is noninterest income the answer? Journal of Money, Credit and Banking, pp.853-882; Albertazzi, U. and Gambacorta, L., 2009. Bank profitability and the business cycle. Journal of Financial Stability, 5(4), pp.393-409.

[^5]: For example, the estimation sample of the Board’s regression models using FR Y-9C generally begins in 1991.

[^6]: Some academic studies evaluate persistence of earnings. For example, Berger, Bonime, Covitz and Hancock (2000) examine return on assets, return on equity, and revenues to costs ratios as measures of firm profitability and find that the persistence of earnings in the banking industry increased into the late 1990s. They note the amount of persistence may be cyclical, decreasing in recessions and increasing in booms. More recently, Goddard, Liu, Molyneux and Wilson (2011) find evidence for persistence in return on equity but document lower rates of persistence in more developed countries. See Berger, A.N., Bonime, S.D., Covitz, D.M. and Hancock, D., 2000. Why are bank profits so persistent? The roles of product market competition, informational opacity, and regional/macroeconomic shocks. Journal of Banking & Finance, 24(7), pp.1203-1235.; Goddard, J., Liu, H., Molyneux, P. and Wilson, J.O., 2011. The persistence of bank profit. Journal of Banking & Finance, 35(11), pp.2881-2890.

[^7]: The Bayesian Information Criterion is a statistical measure typically used in model selection to avoid overfitting a regression model. The criterion prioritizes goodness of fit but penalizes complexity (see Schwarz, G., 1978. Estimating the dimension of a model. *The Annals of Statistics*, pp.461-464). The equation for calculating the BIC is BIC = -2 lnL + k lnN, where lnL is the maximized log-likelihood of the model, k is the number of parameters estimated, and N is the sample size. When comparing two models, a lower BIC would indicate the preferred specification, because either the likelihood is higher, the number of parameters is lower, or both. Intuitively, a higher likelihood implies a lower BIC.

[^8]: For example, some studies explore sensitivity of banks’ performance to interest rates by regressing stock returns on unexpected interest rate changes (Flannery and James (1984), Aharony, Saunders and Swary (1986), Saunders and Yourougou (1990), and Yourougou (1990)). English, Van den Heuvel and Zakrajsek (2018) identified a negative effect of interest rate changes on the common stock returns of financial institutions. The Journal of Finance, 39(4), pp.1141-1153; Aharony, J., Saunders, A. and Swary, I., 1986. The effects of a shift in monetary policy regime on the profitability and risk of commercial banks. Journal of Monetary Economics, 17(3), pp.363-377; Saunders, A. and Yourougou, P., 1990. Are banks special? The separation of banking from commerce and interest rate risk. Journal of Economics and Business, 42(2), pp.171-182. Yourougou, P., 1990. Interest-rate risk and the pricing of depository financial intermediary common stock: Empirical evidence. Journal of Banking & Finance, 14(4), pp.803-820; English, W.B., Van den Heuvel, S.J. and Zakrajšek, E., 2018. Interest rate risk and bank equity valuations. Journal of Monetary Economics, 98, pp.80-97. Demirgüç-Kunt, A. and Huizinga, H., 1999. Determinants of commercial bank interest margins and profitability: some international evidence. The World Bank Economic Review, 13(2), pp.379-408.

[^9]: For example, the textbooks of Stephen G. Cecchetti “Money, banking and financial markets,” 2006, or Frederic S. Mishkin “The economics of money, banking and financial markets,” 2013.

[^10]: The Board considers transformations of macroeconomic variables such as lags, an interaction term with an indicator variable for negative GDP growth, year-over-year growth, quadratic terms, and natural logarithms. The Board also considers two separated independent variables for positive and negative values of each macroeconomic variable.

[^11]: The Board takes several steps to reduce dimensionality when choosing additional macroeconomic variables and their transformations. First, the Board selects one single transformation of each macroeconomic variable, based on the lowest Bayesian Information Criterion. Second, the Board selects only one of highly correlated sets of variables. Third, the Board selects the contemporaneous variable over the lagged variable if both are statistically significant. The exception is that models may include both the level and the change in a macroeconomic variable, as the change includes information from previous period. Finally, the Board includes interest rate variables, other than the 3-month U.S. Treasury rate, only as spreads (i.e., the difference of a certain rate to the 3-month U.S. Treasury rate).

[^12]: The Board considers the joint significance of these calendar quarter indicator variables to determine whether to include them in the model for a particular component.

[^13]: The preferred metric of fit is nine-quarter, out-of-sample, root mean squared error. The Board prioritizes firm-level model fit, followed by aggregate industry model fit. The former assigns higher weight to firm-level performance of large firms, while the latter allows forecasting errors to cancel out across firms and reflects the industry aggregate forecasting error. The choice of the 5% threshold is oriented by practical purposes and based on simplicity.

[^14]: The Board also evaluates in-sample fitting as a secondary measure, for all observations, as well as post-2010, during National Bureau of Economic Research (NBER) recessions, and in the 2008 financial crisis period. The last two metrics are useful for a stress testing forecasting model, because they assess performance during depressed economic cycles.

[^15]: The Board uses the following metrics to evaluate performance: firm-level and industry out-of-sample root-mean squared error, for nine-quarter ahead projections and seven-quarter ahead projections considering specific recession periods. The metrics are computed both in ratios and in dollars.

[^16]: Data for interest income on loans is sourced from form FR Y-9C, corresponding to variable codes BHCK4435, BHCK4436, BHCKF821, BHCK4059 and BHCK4065. Total loans correspond to data variable code BHCK2122 in form FR Y-9C.

[^17]: Per FR Y-9C reporting instructions, this line item represents “the amount of interest income received or accrued during the reporting period on balances carried with domestic and foreign banks and other depository institutions in the United States. Also includes premiums received or discounts paid on foreign exchange contracts related to financial swap transactions involving interest bearing balances due from depository institutions. Such gains or losses are known at the inception of the contract and should be amortized over the life of the contract.” Data for this component is sourced from form FR Y-9C, corresponding to variable code BHCK4115.

[^18]: Data for interest income on U.S. Treasuries is sourced from form FR Y-9C, corresponding to variable code BHCKB488. Balances of U.S. Treasury Securities correspond to the sum of data variable codes BHCK0211, BHCKHT50, BHCK1287, and BHCKHT53 in form FR Y-9C.

[^19]: Data for interest income on mortgage-backed securities is sourced from form FR Y-9C, corresponding to variable code BHCKB489. The balances of mortgage-backed securities correspond to the sum of data variable codes BHCKG300, BHCKG304, BHCKG308, BHCKG312, BHCKG316, BHCKG320, BHCKK142, BHCKK146, BHCKK150, BHCKK154, BHCKG303, BHCKG307, BHCKG311, BHCKG315, BHCKG319, BHCKG323, BHCKK145, BHCKK149, BHCKK153, and BHCKK157 in form FR Y-9C.

[^20]: Such as GNMA (Government National Mortgage Association or Ginnie Mae) which is within the Department of Housing and Urban Development.

[^21]: Such as FNMA (Federal National Mortgage Association or Fannie Mae) and FHLMC (Federal Home Loan Mortgage Corporation or Freddie Mac).

[^22]: Data for interest income on other securities is sourced from form FR Y-9C, corresponding to variable code BHCK4060. The balances of other securities correspond to the sum of data variable codes BHCK1737, BHCK1742, BHCKC026, BHCKT58, BHCK1741, BHCK1746, BHCKA511, BHCKC027, BHCKT61, BHCK8496, BHCK8499, and BHCKJA22 in form FR Y-9C.

[^23]: Data for interest income on trading assets is sourced from form FR Y-9C, corresponding to variable code BHCK4069.

[^24]: Firms that (a) regularly underwrite or deal in securities, interest rate contracts, foreign exchange rate contracts, other off-balance sheet commodity and equity contracts, other financial instruments, and other assets for resale, (b) acquire or take positions in such items principally for the purpose of selling in the near term or otherwise with the intent to resell in order to profit from short-term price movements, or (c) acquire or take positions in such items as an accommodation to customers or for other trading purposes shall report in this item the value of such assets or positions on the report date. Assets and other financial instruments held for trading shall be consistently valued at fair value (or, if appropriate, at the lower of cost or fair value). The balances of trading assets correspond to data variable code BHCK3545 in form FR Y-9C.

[^25]: Data for all other interest income is sourced from form FR Y-9C, corresponding to variable code BHCK4518.

[^26]: The balances of total interest earning assets correspond to the sum of data variable codes BHCK2122, BHDMb987, BHCKb989, BHCK1754, BHCK1773, BHCK0395, BHCK0397, and BHCK3545 in form FR Y-9C.

[^27]: Data for interest expense on domestic time deposits is sourced from form FR Y-9C, corresponding to the sum of variable codes BHCKHK03 and BHCKHK04. The balances of domestic time deposits correspond to the sum of data variable codes BHCBJ474, BHODJ474, BHCBHK29, and BHODHK29 in form FR Y-9C.

[^28]: See Flannery, M.J. and James, C.M., 1984. The effect of interest rate changes on the common stock returns of financial institutions. The Journal of Finance, 39(4), pp.1141-1153.

[^29]: Data for interest expense on other domestic deposits is sourced from form FR Y-9C, corresponding to the variable code BHCK6761. The balances of other domestic deposits correspond to the sum of data variable codes BHCB3187, BHOD3187, BHCB2389, and BHOD2389 in form FR Y-9C.

[^30]: See Hirtle, Beverly, and Matthew C. Plosser. 2025. Bank Economic Capital. Federal Reserve Bank of New York Staff Reports, no. 1144, September.

[^31]: Data for interest expense on foreign deposits is sourced from form FR Y-9C, corresponding to the variable code BHCK4172. The balances of foreign deposits correspond to the sum of data variable codes BHFN6631 and BHFN6636 in form FR Y-9C.

[^32]: See Choi, Dong Beom, and Hyun-Soo Choi, 2021. The effect of monetary policy on bank wholesale funding. Management Science 67(1), pp.388-416.

[^33]: The combination of interest expense on trading liabilities and other borrowed money with all other interest expense into one single component for projection is consistent with the quarterly Bank Holding Company Performance Report (BHCPR) which already combines expenses of both accounts into a single line.

[^34]: Data for interest expense on trading liabilities, other borrowed money, and all other interest expense is sourced from form FR Y-9C, corresponding to variable codes BHCK4185 and BHCK4398. The balances of trading liabilities and other borrowed money correspond to the sum of data variable codes BHCK3548 and BHCK3190 in form FR Y-9C.

[^35]: The amount reported in this item equals the sum of items BHCK8757, BHCK8758, BHCK8759, and BHCK8760 from FR Y-9C. The following are included as trading revenue: (1) revaluation adjustments to the carrying value of assets and liabilities reported in item BHCK3545 and in item BHCK3548, resulting from the periodic marking to market of such assets and liabilities; (2) revaluation adjustments from the periodic marking to market of interest rate, foreign exchange rate, commodity, and equity derivative contracts reportable in Schedule RC-L, item 13, "Total gross notional amount of derivative contracts held for trading" and credit derivative contracts reportable in Schedule RC-L, item 7, "Credit derivatives," that are held for trading purposes; and (3) incidental income and expense related to the purchase and sale of cash instruments reportable in Schedule RC, item 5, "Trading assets," and Schedule RC, item 15, "Trading liabilities, derivative contracts reportable in Schedule RC-L, item 13, "Total gross notional amount of derivative contracts held for trading," and credit derivative contracts reportable in Schedule RC-L, item 7, "Credit derivatives," that are held for trading. If the amount reported is a net loss, then it is enclosed in parentheses.

[^36]: Gebka, B., 2025. Explaining the causality between trading volume and stock returns: What drives its cross-quantile patterns? Economic Modelling, 148. Falato, A., Iercosan, D., and Zikes, F., 2025. Banks as regulated traders. Journal of Financial Economics, 170. Lu, L., and Wallen, J., 2024. What Do Bank Trading Desks Do? Harvard Business School Working Paper. Modig, Z., Inanoglu, H., and Lynch, D., 2025. Impact of the Volcker Rule on the Trading Revenue of Largest U.S. Trading Firms During the COVID-19 Crisis Period. Finance and Economics Discussion Series, 2025–005, 1–1.

[^37]: Data for noninterest income on service charges on deposits is sourced from form FR Y-9C, corresponding to variable code BHCK4483. The balances of total deposits correspond to the sum of data variable codes BHDM6631, BHDM6636, BHFN6631, and BHFN6636 in form FR Y-9C.

[^38]: Data for noninterest income on net servicing fees is sourced from form FR Y-9C, corresponding to variable code BHCKB492. The balances of total servicing assets correspond to data variable code BHCK3164 in form FR Y-9C.

[^39]: Noninterest income from investment banking fees is computed as the sum of commissions from securities brokerage (BHCKC886), underwriting fees (BHCKC888), and venture capital revenue (BHCKB491). The Board projects this component as the ratio of this income normalized by the balance of total assets (BHCK2170). All data is from FR Y-9C or Call Reports.

[^40]: Noninterest income from fiduciary income and insurance banking fees consists of income from fiduciary activities (BHCK4070), fees and commissions from annuity sales (BHCKC887), underwriting income from insurance and reinsurance activities (BHCKC386), and income from other insurance activities (BHCKC387). The Board projects this component as the ratio of this income normalized by the balance of total assets (BHCK2170) less trading assets (BHCK3545). All data is from FR Y-9C or Call Reports.

[^41]: Noninterest expense on compensation corresponds to data variable code BHCK4135 in form FR Y-9C. Total assets correspond to data variable code BHCK2170 in form FR Y-9C.

[^42]: The efficiency ratio is a commonly used measure for efficiency in the banking industry. It measures how effectively a bank manages its expenses relative to its revenue, with lower ratios indicating greater efficiency. It is calculated by dividing noninterest expenses by a measure of revenue (for example, total revenue or net operating revenue). A lower ratio means the bank spends less to generate each dollar of revenue, which is generally desirable.

[^43]: Data for noninterest expense on fixed assets is sourced from form FR Y-9C, corresponding to variable code BHCK4217. The balances of total assets correspond to data variable code BHCK2170 in form FR Y-9C.

[^44]: The efficiency ratio is a commonly used measure for efficiency in the banking industry. It measures how effectively a bank manages its expenses relative to its revenue, with lower ratios indicating greater efficiency. It is calculated by dividing noninterest expenses by a measure of revenue (for example, total revenue or net operating revenue). A lower ratio means the bank spends less to generate each dollar of revenue, which is generally desirable.

[^45]: Data for interest income from federal funds sold and securities purchased under agreements to resell is sourced from form FR Y-9C, corresponding to variable code BHCK4020. The balances assets for federal funds sold and securities purchased under the agreement to resell correspond to the sum of data variable codes BDMB987 and BHCKB989 in form FR Y-9C.

[^46]: The above derivation is agnostic about the rate that firms earn on their federal funds sold and securities purchased under agreements to resell, as this rate may be at, below, or above SOFR or the federal funds rate.

[^47]: Data for interest income from federal funds purchased and securities sold under agreements to repurchase is sourced from form FR Y-9C, corresponding to variable code BHCK4180.

[^48]: The balances for liabilities underlying federal funds purchased and securities sold under the agreement to repurchase correspond to the sum of data variable codes BDMB9993 and BHCKB995 in form FR Y-9C.

[^49]: See Acharya, V.V., Gujral, I., Kulkarni, N. and Shin, H.S., 2011. Dividends and bank capital in the financial crisis of 2007-2009 (No. w16896). National Bureau of Economic Research.

[^50]: Form FR Y-9C variable BHCK4397. Subordinated debt notes provide flexibility in their term structure, which allows firms to adjust their holdings based on their hedging strategy and funding needs. These notes are issued and held at an agreed upon rate or set of rates for a fixed amount of time until expiration or maturity. Rates can be fixed, variable and linked to a benchmark or reference rate, have step-up changes, or be convertible.

[^51]: Security-level end-of-quarter holdings of subordinated debt are reported on Schedule A of FR Y-14Q. Firm redemptions and issuances are reported on FR Y-14Q Schedules B and C, respectively.

[^52]: See Supervisory Stress Test Model Documentation, Market Risk Models, the Yield Curve Model section.

[^53]: This formula approximates accrual-based accounting practices whereby the expense is evenly recognized throughout the year regardless of the actual interest (known as “coupon”) payment schedule.

[^54]: The coupon rate is always an annual rate divided by four to reflect the even accrual of interest over the year consistent with U.S. GAAP and the fact that coupon rates are always stated as annualized rates.

[^55]: Reference rates, such as the 3-month Secured Overnight Financing Rate (SOFR) and some other rates, e.g., EURIBOR and Fed Funds, are included in the scenario. If a relevant reference rate is not forecasted because it is a foreign security, such as Australian BBSW, the foreign rate is defined as SOFR plus the tenor-consistent SOFR spread plus the spread of the foreign rate over SOFR. The People’s Bank of China (PBOC) prime lending rate and the Singaporean Swap Offer Rate (SSOR) are assumed to be constant over the forecast horizon.

[^57]: Data for total assets balances is sourced from form FR Y-9C, corresponding to variable code BHCK2170.

[^58]: The Board separately models losses from operational risk and other real estate owned (OREO) expenses. Operational risk is defined as “the risk of loss resulting from inadequate or failed internal processes, people and systems, or from external events.” OREO expenses are those expenses related to the disposition of real estate owned properties and stem from losses on first-lien mortgages. OREO expenses are based on losses projected by the first-lien mortgage model, which is discussed in the “Loan Losses and Provisions on Loans Measured at Amortized Cost” section.

[^59]: Operational risk expenses are excluded from total noninterest expense using data on operational losses available in FR Y-14Q Schedule G.

[^60]: The efficiency ratio is a commonly used measure for efficiency in the banking industry. It measures how effectively a bank manages its expenses relative to its revenue, with lower ratios indicating greater efficiency. It is calculated by dividing noninterest expenses by a measure of revenue (for example, total revenue or net operating revenue). A lower ratio means the bank spends less to generate each dollar of revenue, which is generally desirable.

[^61]: The wholesale FR Y-14Q data is at the facility level, but for ease of readability by matching with Retail this document references FR Y-14Q data as at the loan level.

[^62]: The wholesale FR Y-14Q interest rate variability value for variable-rate is floating. Using variable-rate in this document for ease of readability.

[^63]: The Board calculates an industry-level scalar separately for mortgage, auto, corporate & investment, small and median business loans and card, domestic CRE, consumer credit card, one category for rest of consumer loans, and one for rest of wholesale exposures.

[^64]: *See* Securities Model Description.

[^65]: For additional details on the incorporation of macroeconomic variables into the vendor model, please refer to the Securities Model Description.

[^66]: For instance, stock in Federal Reserve Banks yields the lesser of six percent and the 10-year Treasury yield. Notes: Statistical significance levels of 1%, 5%, and 10% are indicated as ***, **, and *, respectively.

[^67]: If the component is one for which there is no scaling balance, this quantity is set to 1.

[^68]: Note that with a linear model, efficiency ratios above 100% are possible, which would then imply negative net noninterest income for the firm in that quarter. Some firms report projections with efficiency ratios above 100%, and negative PPNR (and ERs above 100%) was observed for some firms in the 2008 financial crisis.

[^69]: The quarterly change in the unemployment rate is defined as Quarterly_Change_X(t) = X(t) - X(t-1).

[^70]: The quarterly change in the Dow Jones Total Stock Market Index is defined as Quarterly_Change_X(t) = [ X(t) / X(t-1)] - 1.

[^71]: The cumulative change in the Dow Jones Total Stock Market Index is defined as Cumulative_Change_X(t) = [ X(t) / X(0)] - 1.

[^72]: The cumulative change in Real GDP is defined as follows. Let AGR(q) be the annual GDP growth rate as published in the scenario for quarters q=1, 2,..., 9. Then the corresponding cumulative change for quarter (t) is: $\prod_{q=1}^{t}\left\{\left(1+\frac{AGR_q}{100}\right)^{0.25}\right\}$.

[^73]: The quarterly change in the 10-year Treasury yield is defined as Quarterly_Change_X(t) = X(t) - X(t-1).

