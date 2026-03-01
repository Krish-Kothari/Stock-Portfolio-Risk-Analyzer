

# 🧩 Problem Statement
What is the Problem?
Most everyday people (like students, young professionals, or first-time investors) invest in stocks without really understanding how risky their portfolio is. They see their money go up and down but don't know why or what to do about it.
Why Does This Problem Exist?

📉 Too complex — Risk analysis tools like Bloomberg Terminal cost thousands of dollars per year
🧮 Hard math — Metrics like Sharpe Ratio, Beta, and VaR sound scary and confusing
🔒 No access — Most powerful tools are only available to banks and big investment firms
📊 No visuals — Raw stock data is just numbers — hard to understand without charts

# Real-World Impact
Impact AreaDescription💸 Financial LossRetail investors lose money because they don't know their portfolio is too risky😰 Emotional StressMarket crashes cause panic because investors don't understand their exposure📚 Knowledge GapFirst-time investors have no tool to learn about risk while investing🏦 Business GapNo free, beginner-friendly risk analyzer exists in the market

Bottom line: Everyday investors need a simple, free, and visual tool to understand and manage portfolio risk — and that's exactly what we built.


# 💡 Proposed Solution
What Did We Build?
Stock Portfolio Risk Analyzer is a full-stack web application where users can:

Add their stocks and quantities
Get real-time prices automatically
See their total portfolio value
Understand their risk level through simple visualizations

How Does It Solve the Problem?
Instead of showing scary numbers, our app:

✅ Translates complex metrics into simple language ("Your portfolio is Medium Risk")
✅ Shows color-coded charts (Green = Safe, Red = Risky)
✅ Gives actionable alerts ("You have 70% in Tech stocks — consider diversifying!")
✅ Is completely free to use

# ✨ Key Features

📡 Real-Time Stock Data — Fetches live prices using Alpha Vantage / Yahoo Finance API
📊 Risk Metrics Dashboard — Shows Volatility, Beta, Sharpe Ratio, and Value at Risk (VaR)
🥧 Diversification Analysis — Pie charts showing sector-wise portfolio split
🎨 Visual Risk Dashboard — Beautiful charts built with Recharts / Chart.js
🚨 Risk Alerts — Warns users when a single stock or sector is too dominant
🔐 Secure Login — JWT-based authentication to save your portfolio
📱 Responsive Design — Works on mobile and desktop


# 🛠️ Tech Stack
LayerTechnologyWhy We Used It🎨 FrontendReact.js + TailwindCSSFast, component-based UI with clean styling📊 ChartsRecharts / Chart.jsBeautiful, responsive financial charts⚙️ BackendNode.js + ExpressLightweight REST API server🗄️ DatabasePostgreSQLStores user accounts and portfolio data📈 Stock APIsAlpha Vantage / Yahoo Finance / FinnhubReal-time stock price data🔐 AuthJWT (JSON Web Tokens)Secure user login and session management🚀 Frontend DeployVercelFree, fast deployment for React apps🖥️ Backend DeployRender / RailwayFree Node.js backend hosting

# 🏗️ System Architecture
┌─────────────────────────────────────────────────────────────────┐
│                        USER (Browser)                           │
│                 Opens the index.html Web App                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP Request
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FRONTEND (html,css)                           │
│                 CSS UI + Recharts Visualizations                │
│  - Portfolio Input Form                                         │
│  - Risk Dashboard with Charts                                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │ REST API Call (fetch/axios)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  BACKEND (Node.js + Express)                    │
│                     REST API Server                             │
│  ┌─────────────────┐  ┌──────────────────┐   ┌───────────────┐  │
│  │   Auth Routes   │  │  Portfolio Routes│   │  Risk Engine  │  │
│  │  /login/signup  │  │  /add /delete    |   │  Calculates   │  │
│  │   JWT tokens    │  │  /getPortfolio   │   │  VaR, Beta,   │  │
│  └─────────────────┘  └──────────────────┘   │  Sharpe Ratio │  │
│                                              └───────────────┘  │
└──────────——───────────────────────┬────────────────────────────-┘
                                    │
                                    ▼
                        ┌───────────────────────────────┐
                        │     External Stock APIs       │
                        │                               │
                        │    Yahoo Finance API          │
                        │  (Real-time price data)       │
                        └───────────────────────────────┘
                        
# Component Roles
ComponentRoleReact FrontendShows the UI, sends requests to backend, displays chartsExpress BackendHandles all business logic, routes, and API callsRisk Calculation EnginePure JavaScript functions that compute risk metricsPostgreSQL DatabaseStores user accounts and their saved portfoliosExternal Stock APIsProvides real-time and historical stock price data

# 🔄 Data Flow
Here's how data moves through the system step by step:
# Step 1: USER INPUT
        User enters stock symbols (e.g., AAPL, TSLA) and quantities
        on the React frontend form
              ↓

# Step 2: API REQUEST
        Frontend sends a POST request to our backend:
        POST /api/portfolio/analyze
        Body: { stocks: [{ symbol: "AAPL", qty: 10 }, ...] }
              ↓

# Step 3: FETCH REAL-TIME DATA
        Backend calls Alpha Vantage / Yahoo Finance API
        to get current prices and historical data for each stock
              ↓

# Step 4: RISK CALCULATION
        Risk Engine processes the data and calculates:
        → Volatility (how much the stock price moves)
        → Beta (how it moves compared to the market)
        → Sharpe Ratio (return vs risk score)
        → VaR (maximum expected loss in a day/week)
              ↓

# Step 5: DATABASE SAVE
        Results and portfolio are saved in PostgreSQL
        linked to the logged-in user's account
              ↓

# Step 6: RESPONSE TO FRONTEND
        Backend sends back a clean JSON response with
        all calculated metrics and chart-ready data
              ↓

# Step 7: VISUALIZATION
        React renders charts, pie graphs, and risk badges
        User sees their portfolio risk in a simple dashboard

# ✨ Key Features

📡 Real-Time Stock Prices — Live data from financial APIs, updated every time you analyze
📊 Volatility Score — See how "jumpy" your stocks are on a simple scale
⚖️ Beta Analysis — Understand how your portfolio moves with the overall market
💹 Sharpe Ratio — Know if you're getting good returns for the risk you're taking
🎯 Value at Risk (VaR) — See the maximum you could lose on a bad day
🥧 Diversification Pie Chart — Visual breakdown of your portfolio by sector
🚨 Smart Risk Alerts — Automatic warnings when your portfolio is too concentrated
🔐 User Authentication — Secure login with JWT so your data is private
💾 Save & Track — Save multiple portfolios and track them over time
📱 Mobile Friendly — Fully responsive design, works on any device
