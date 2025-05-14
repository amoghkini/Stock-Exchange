# Stock-Exchange

docker commands
1. docker-compose down --volumes --remove-orphans
2. docker system prune -a --volumes

3. docker-compose up -d
4. docker-compose -f docker-compose-dev.yaml up -d



TODO: 
a list of possible microservices you might need to build an exchange platform:

1. User Management Service:

Handles user registration, authentication, profile management, and account settings.
Integrates with OAuth or other authentication providers.

2. Wallet Service:

Manages users' balances and wallets for different currencies.
Supports deposits, withdrawals, and internal transfers.
Monitors wallet addresses and confirms transactions.

3. Order Matching Engine:

Matches buy and sell orders based on price and time priority.
Manages the order book and trade execution.

4. Trading API Gateway:

Exposes public and private APIs for users to place orders, cancel orders, and check balances.
Provides WebSocket and RESTful endpoints for real-time data.

5. Market Data Service:

Aggregates and distributes real-time market data, including order book depth, trades, and historical data.
Supports candlestick and OHLC data generation.

6. Risk Management Service:

Monitors trading activity to detect anomalies, potential market abuse, and risk exposure.
Implements risk rules to limit large orders or rapid trades.

7. Trade Settlement Service:

Handles post-trade processes, including trade confirmation and settlement.
Updates users’ balances after successful trades.

8. Accounting and Ledger Service:

Maintains a comprehensive and immutable ledger of all transactions and balances.
Provides auditing and reconciliation tools.

9. Notification and Alerts Service:

Sends notifications for order updates, trade confirmations, and alerts for unusual activity.
Supports email, SMS, and push notifications.

10. Analytics and Reporting Service:

Generates detailed trading reports, P&L analysis, and user statistics.
Provides data analytics and visualization for market trends.

12. Fee and Commission Service:

Calculates trading fees, withdrawal fees, and commissions based on configured rules.
Updates the ledger accordingly.

13. Liquidity Management Service:

Ensures adequate liquidity in the order book by placing automated buy and sell orders.
Integrates with external liquidity providers if needed.

14. Monitoring and Logging Service:

Monitors the health and performance of all microservices.
Centralizes logs for auditing and troubleshooting.

15. Admin and Dashboard Service:

Provides admin users with an interface to monitor the platform, manage users, and configure fees.
Displays metrics, statistics, and system health.

16. Payment Gateway Integration Service:

Integrates with banks and payment providers to process fiat deposits and withdrawals.

17. Data Archival and Backup Service:

Archives historical data and provides backup and restoration capabilities.
