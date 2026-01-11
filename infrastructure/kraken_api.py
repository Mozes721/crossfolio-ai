from krakenex import API
from domain.models import Portfolio, Position, AssetClass, Sector


class KrakenClient:
    # Map asset codes to their correct pair names
    PAIR_MAPPING = {
        'XXBT': 'XBTUSD',
        'XETH': 'XETHZUSD',
        'PEPE': 'PEPEUSD',
        'SOL': 'SOLUSD',
        'ADA': 'ADAUSD',
        'DOT': 'DOTUSD',
        'MATIC': 'MATICUSD',
        'LINK': 'LINKUSD',
    }
    
    def __init__(self, api_key: str, private_key: str):
        self.client = API(key=api_key, secret=private_key)

    def get_portfolio(self) -> Portfolio:
        balance_response = self.client.query_private('Balance')
        
        if balance_response.get('error'):
            raise ValueError(f"Kraken API error: {balance_response['error']}")
        
        balances = balance_response.get('result', {})
        
        # Get all crypto balances (exclude fiat starting with Z)
        crypto_assets = {
            asset: float(qty) 
            for asset, qty in balances.items() 
            if not asset.startswith('Z') and float(qty) > 0
        }
        
        if not crypto_assets:
            return Portfolio(positions=[])
        
        # Fetch all prices at once
        prices = self._get_prices(crypto_assets.keys())
        
        # Build positions
        positions = []
        for asset, quantity in crypto_assets.items():
            price = prices.get(asset, 0.0)
            
            if price == 0.0:
                print(f"Warning: No price found for {asset}, skipping")
                continue
            
            position = Position(
                ticker=self._clean_ticker(asset),
                quantity=quantity,
                avg_price=price,
                current_price=price,
                asset_class=AssetClass.CRYPTO,
                sector=Sector.OTHER
            )
            positions.append(position)
        
        return Portfolio(positions=positions)

    def _get_prices(self, assets: list) -> dict:
        """Fetch USD prices for all assets in one API call."""
        prices = {}
        
        # Build list of pairs we can fetch
        pairs_to_fetch = []
        asset_to_pair = {}
        
        for asset in assets:
            pair = self.PAIR_MAPPING.get(asset)
            if pair:
                pairs_to_fetch.append(pair)
                asset_to_pair[asset] = pair
            else:
                # Try generic {asset}USD format for unknown assets
                pair = f"{asset}USD"
                pairs_to_fetch.append(pair)
                asset_to_pair[asset] = pair
        
        if not pairs_to_fetch:
            return prices
        
        # Single API call
        response = self.client.query_public('Ticker', {'pair': ','.join(pairs_to_fetch)})
        
        if response.get('error'):
            return prices
        
        # Parse prices
        result = response.get('result', {})
        for asset, pair in asset_to_pair.items():
            # Kraken might return the pair name or a variant (XBTUSD -> XBTZUSD)
            data = result.get(pair) or result.get(pair.replace('USD', 'ZUSD'))
            if data and data.get('c'):
                prices[asset] = float(data['c'][0])
            else:
                # Debug: check what pairs were actually returned
                print(f"Debug: No price data for {asset} (tried pair: {pair})")
                print(f"Debug: Available pairs in response: {list(result.keys())[:5]}")
        
        return prices

    def _clean_ticker(self, asset: str) -> str:
        """Convert Kraken asset code to readable ticker."""
        if asset == 'XXBT':
            return 'BTC'
        
        # Strip X prefix for most assets
        return asset.lstrip('X')