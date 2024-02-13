
from flask_apscheduler import APScheduler


schedule = APScheduler()


def process_trades():
    with app.app_context():
        try:
            # Query all active trades
            active_trades = (
                db.session.query(Order)
                .filter_by(is_active=True)
                .all()
            )

            # Categorize trades based on trade_type
            buy_trades = [trade for trade in active_trades if trade.trade_type == "buy"]
            sell_trades = [trade for trade in active_trades if trade.trade_type == "sell"]

            # Calculate the sum of trading_amount for each category
            buy_sum = sum(trade.trading_amount for trade in buy_trades)
            sell_sum = sum(trade.trading_amount for trade in sell_trades)

            # Determine the category with the highest and lowest sum trading_amount
            winning_category = "buy" if buy_sum < sell_sum else "sell"
            losing_category = "buy" if buy_sum >= sell_sum else "sell"

            # Update trades with status, calculate profit and new balance, and set closing_time
            for trade in active_trades:
                if trade.trade_type == winning_category:
                    trade.status = "won"
                    trade.profit = (trade.trading_amount * 1.65) - trade.trading_amount

                    # Add profit and trading amount to the user's balance for winning trades
                    current_user = User.query.get(trade.user_id)
                    current_user.balance += trade.profit + trade.trading_amount

                elif trade.trade_type == losing_category:
                    trade.status = "lost"
                    trade.profit = 0  # No profit for losing trades

                # Mark trade as not active to prevent using it multiple times
                trade.is_active = False

                # Set closing_time to the current time
                trade.closing_time = datetime.now(timezone.utc).time()

            db.session.commit()

        except Exception as e:
            print(f"An error occurred while processing trades: {e}")


# Add this line to the __main__ block to schedule the process_trades function
schedule.add_job(id='process_trades', func=process_trades, trigger='interval', minutes=5)
schedule.start()
