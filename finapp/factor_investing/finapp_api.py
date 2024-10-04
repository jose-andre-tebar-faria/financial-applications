import finapp_controller as fc
import telegram_user_manager as tum
import wallet_manager as wm

import pandas as pd

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/setups/<string:username>', methods=['GET'])
def setups(username):
    
    wallet_manager = wm.WalletManager()
    
    wallet_id = request.args.get('wallet_id')

    file_not_found, wallets_df = wallet_manager.read_setups(username)
    
    if file_not_found:
        return jsonify({"error": "File not found"}), 404
    else:
        if wallets_df.empty:
            return jsonify({"error": "No data available for the selected date range."}), 404
        
        wallets_df = wallets_df.drop(['actual_wallet_total_number_of_assets', 'last_rebalance_date', 'close_date'], axis=1)

        if wallet_id:
            wallets_df = wallets_df[wallets_df['wallet_id']==str(wallet_id)]
        # print(wallets_df)

        wallets_df = wallets_df.to_dict(orient='records')
        return jsonify(wallets_df)

@app.route('/portifolios/<string:username>/<int:wallet_id>', methods=['GET'])
def portifolios(username, wallet_id):

    wallet_manager = wm.WalletManager()

    start_date = request.args.get('start_date')  # Data de início (opcional)
    end_date = request.args.get('end_date') 

    file_not_found, compositions_df = wallet_manager.read_portifolios_composition(wallet_id)
    compositions_df = compositions_df.drop(['execution_date', 'executed'], axis=1)

    if file_not_found:
        return jsonify({"error": "File not found"}), 404
    else:
        compositions_df['rebalance_date'] = pd.to_datetime(compositions_df['rebalance_date'])

        if start_date:
                start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
                compositions_df = compositions_df[compositions_df['rebalance_date'] >= start_date]
            
        if end_date:
            end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
            compositions_df = compositions_df[compositions_df['rebalance_date'] <= end_date]

        if compositions_df.empty:
            return jsonify({"error": "No data available for the selected date range."}), 404
        
        compositions_df = compositions_df.sort_values(by='rebalance_date', ascending=False)
        # print(compositions_df)

        compositions_df = compositions_df.groupby('rebalance_date').apply(lambda x: x.drop(columns=['rebalance_date', 'wallet_id']).to_dict(orient='records')).sort_index(ascending=False).to_dict()

        compositions_df_list = [{"rebalance_date": str(key.date()), "content": value} for key, value in compositions_df.items()]

        response = {
            "total_rebalances": len(compositions_df_list),
            "portifolios": compositions_df_list
        }

        return jsonify(response)

app.run(port=5000, host='localhost', debug=True)