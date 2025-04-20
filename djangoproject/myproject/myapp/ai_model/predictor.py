import pandas as pd
from joblib import load
import datetime

def get_best_sell_date(district, state, market, commodity, variety):
    # Load model and columns
    model, columns = load('myapp/ai_model/price_predictor.joblib')
    
    today = datetime.date.today()
    data_points = []
    
    for i in range(30):
        future_date = today + datetime.timedelta(days=i)
        test_row = {
            'Month': future_date.month,
            'Day': future_date.day,
            'Weekday': future_date.weekday(),
            'Date_Ordinal': future_date.toordinal(),
            'District Name': district,
            'State': state,
            'Market Name': market,
            'Commodity': commodity,
            'Variety': variety
        }
        
        df = pd.DataFrame([test_row])
        df = pd.get_dummies(df)
        
        # Ensure all model columns exist
        for col in columns:
            if col not in df.columns:
                df[col] = 0
        df = df[columns]  # correct column order
        
        pred_price = model.predict(df)[0]
        print(f"{future_date}: Rs.{pred_price:.2f}/Quintal")  # Log all predictions
        data_points.append((future_date, pred_price))
    
    # Find best day
    best_day = max(data_points, key=lambda x: x[1])
    
    # Return both best_day and data_points
    return best_day, data_points