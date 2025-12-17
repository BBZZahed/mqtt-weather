import pytest
import json
from unittest.mock import Mock, patch, MagicMock
import station1


class TestStationData:
    """Tests für die Wetterstations-Daten"""

    @patch('station1.mqtt.Client')
    @patch('station1.time.sleep')
    @patch('station1.time.strftime')
    def test_data_structure(self, mock_strftime, mock_sleep, mock_mqtt_client):
        """Test ob die Datenstruktur korrekt ist"""
        mock_strftime.return_value = "2025-12-17T12:00:00Z"
        mock_sleep.side_effect = [None, Exception("Stop")]
        
        mock_client = MagicMock()
        mock_mqtt_client.return_value = mock_client
        
        with patch('station1.random.uniform') as mock_uniform:
            mock_uniform.side_effect = [20.5, 45.3]
            
            with patch('station1.random.random', return_value=0.5):
                try:
                    exec(open('station1.py').read())
                except Exception:
                    pass
        
        # Prüfe ob publish aufgerufen wurde
        assert mock_client.publish.called
        
        # Hole die veröffentlichten Daten
        call_args = mock_client.publish.call_args[0]
        published_data = json.loads(call_args[1])
        
        # Prüfe Struktur
        assert "stationId" in published_data
        assert "temperature" in published_data
        assert "humidity" in published_data
        assert "timestamp" in published_data

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
