def calculate_late_fee(transaction):
    if transaction.return_date and transaction.return_date > transaction.due_date:
        days_late = (transaction.return_date - transaction.due_date).days
        return days_late * 1  # $1 per day late
    return 0
