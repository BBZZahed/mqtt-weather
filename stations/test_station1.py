import json
from unittest.mock import patch, MagicMock


class TestStationData:
    """Tests für die Wetterstations-Daten"""

    def test_data_structure(self):
        """Test ob die Datenstruktur korrekt ist"""
        data = {
            "stationId": "WS-01",
            "temperature": 22.5,
            "humidity": 45.3,
            "timestamp": "2025-12-17T12:00:00Z"
        }
        
        # DIESER TEST WIRD FEHLSCHLAGEN
        assert data["temperature"] == 100.0  # Falscher Wert!

    def test_temperature_range(self):
        """Test ob Temperaturwerte im erwarteten Bereich liegen"""
        import random
        random.seed(42)

        for _ in range(100):
            if random.random() >= 0.01:
                temp = round(random.uniform(15, 30), 1)
                assert 15 <= temp <= 30

    def test_humidity_range(self):
        """Test ob Luftfeuchtigkeitswerte im erwarteten Bereich liegen"""
        import random
        random.seed(42)

        for _ in range(100):
            humidity = round(random.uniform(30, 60), 1)
            assert 30 <= humidity <= 60

    def test_error_temperature_value(self):
        """Test ob Fehlertemperatur -999 ist"""
        error_temp = -999
        assert error_temp == -999

    @patch.dict('os.environ', {'STATION_ID': 'TEST-01', 'INTERVAL': '10'})
    def test_environment_variables(self):
        """Test ob Umgebungsvariablen korrekt gelesen werden"""
        import os
        station_id = os.getenv("STATION_ID", "WS-XX")
        interval = int(os.getenv("INTERVAL", "5"))

        assert station_id == "TEST-01"
        assert interval == 10

    def test_default_environment_variables(self):
        """Test ob Default-Werte korrekt sind"""
        import os
        with patch.dict('os.environ', {}, clear=True):
            station_id = os.getenv("STATION_ID", "WS-XX")
            interval = int(os.getenv("INTERVAL", "5"))

            assert station_id == "WS-XX"
            assert interval == 5

    def test_json_serialization(self):
        """Test ob Daten korrekt als JSON serialisiert werden können"""
        import time
        data = {
            "stationId": "WS-01",
            "temperature": 22.5,
            "humidity": 45.3,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        json_str = json.dumps(data)
        parsed = json.loads(json_str)

        assert parsed["stationId"] == "WS-01"
        assert parsed["temperature"] == 22.5
        assert parsed["humidity"] == 45.3
        assert "timestamp" in parsed
        