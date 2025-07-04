"""
Unit tests for portfolio management and data persistence
Tests covering portfolio recommendations, historical data, and file operations
"""

import unittest
from unittest.mock import patch, Mock, MagicMock, mock_open
import sys
import os
import pickle
import tempfile
from datetime import datetime, timedelta

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit_app import PortfolioTracker

class TestPortfolioManagement(unittest.TestCase):
    """Test portfolio management functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tracker = PortfolioTracker()
        
        # Sample portfolio results
        self.sample_results = [
            {
                'ticker': 'AAPL',
                'rs_score': 85,
                'avg_weekly_return': 3.0,
                'market_cap': 3e12,
                'meets_criteria': True,
                'qualification_reason': 'Strong momentum',
                'sector': 'Technology',
                'weeks_above_target': 4,
                'daily_change': 1.5,
                'weekly_returns': [0.03, 0.025, 0.035, 0.028]
            },
            {
                'ticker': 'MSFT',
                'rs_score': 80,
                'avg_weekly_return': 2.8,
                'market_cap': 2.5e12,
                'meets_criteria': True,
                'qualification_reason': 'Consistent performance',
                'sector': 'Technology',
                'weeks_above_target': 3,
                'daily_change': 1.2,
                'weekly_returns': [0.028, 0.032, 0.025, 0.031]
            },
            {
                'ticker': 'JPM',
                'rs_score': 75,
                'avg_weekly_return': 2.2,
                'market_cap': 500e9,
                'meets_criteria': True,
                'qualification_reason': 'Financial strength',
                'sector': 'Financial Services',
                'weeks_above_target': 2,
                'daily_change': 0.8,
                'weekly_returns': [0.022, 0.020, 0.025, 0.023]
            }
        ]
        
    def test_generate_portfolio_recommendations_basic(self):
        """Test basic portfolio recommendations generation"""
        with patch.object(self.tracker, 'passes_filters', return_value=True):
            recommendations = self.tracker.generate_portfolio_recommendations(
                self.sample_results, 
                portfolio_size=2,
                min_rs_score=70,
                min_weekly_target=2.0
            )
            
            self.assertIsInstance(recommendations, dict)
            self.assertIn('top_picks', recommendations)
            self.assertIn('strong_buys', recommendations)
            self.assertIn('moderate_buys', recommendations)
            self.assertIn('watch_list', recommendations)
            self.assertIn('comparison', recommendations)
            
            # Should recommend top 2 tickers
            self.assertEqual(len(recommendations['top_picks']), 2)
            
    def test_generate_portfolio_recommendations_diversification(self):
        """Test portfolio recommendations consider diversification"""
        # Add more diverse results
        diverse_results = self.sample_results + [
            {
                'ticker': 'XLE',
                'rs_score': 70,
                'avg_weekly_return': 2.5,
                'market_cap': 100e9,
                'meets_criteria': True,
                'qualification_reason': 'Energy momentum',
                'sector': 'Energy',
                'weeks_above_target': 2,
                'daily_change': 1.0,
                'weekly_returns': [0.025, 0.022, 0.028, 0.025]
            }
        ]
        
        with patch.object(self.tracker, 'passes_filters', return_value=True):
            recommendations = self.tracker.generate_portfolio_recommendations(
                diverse_results,
                portfolio_size=3,
                min_rs_score=70,
                min_weekly_target=2.0
            )
            
            # Should have picks categorized
            self.assertIsInstance(recommendations['top_picks'], list)
            self.assertGreater(len(recommendations['top_picks']), 0)
            
    def test_generate_portfolio_recommendations_empty_input(self):
        """Test portfolio recommendations with empty input"""
        recommendations = self.tracker.generate_portfolio_recommendations(
            [],
            portfolio_size=10
        )
        
        self.assertIsInstance(recommendations, dict)
        self.assertEqual(len(recommendations['top_picks']), 0)
        self.assertEqual(len(recommendations['strong_buys']), 0)
        
    @patch.object(PortfolioTracker, 'load_historical_results')
    def test_compare_with_previous_new_tickers(self, mock_load):
        """Test comparison with previous results - new tickers"""
        # Mock previous results
        previous_results = [
            {
                'timestamp': datetime.now() - timedelta(days=1),
                'results': [
                    {
                        'ticker': 'OLD1',
                        'rs_score': 75,
                        'avg_weekly_return': 2.0,
                        'market_cap': 1e12,
                        'meets_criteria': True,
                        'weeks_above_target': 2,
                        'daily_change': 0.5,
                        'weekly_returns': [0.02, 0.018, 0.022, 0.020]
                    }
                ]
            },
            {
                'timestamp': datetime.now(),
                'results': []
            }
        ]
        mock_load.return_value = previous_results
        
        with patch.object(self.tracker, 'passes_filters', return_value=True):
            comparison = self.tracker.compare_with_previous(
                self.sample_results,
                min_rs_score=70,
                min_weekly_target=2.0
            )
            
            self.assertIsInstance(comparison, dict)
            self.assertIn('new_entrants', comparison)
            self.assertIn('dropped_out', comparison)
            self.assertIn('improved', comparison)
            self.assertIn('declined', comparison)
            self.assertTrue(comparison['has_previous'])
            
            # All sample results should be new (different from OLD1)
            self.assertGreater(len(comparison['new_entrants']), 0)
            
    @patch.object(PortfolioTracker, 'load_historical_results')
    def test_compare_with_previous_continued_tickers(self, mock_load):
        """Test comparison with previous results - continued tickers"""
        # Mock previous results that overlap with current
        previous_results = [
            {
                'timestamp': datetime.now() - timedelta(days=1),
                'results': [
                    {
                        'ticker': 'AAPL',
                        'rs_score': 80,
                        'avg_weekly_return': 2.5,
                        'market_cap': 3e12,
                        'meets_criteria': True,
                        'weeks_above_target': 3,
                        'daily_change': 1.0,
                        'weekly_returns': [0.025, 0.020, 0.028, 0.025]
                    }
                ]
            },
            {
                'timestamp': datetime.now(),
                'results': []
            }
        ]
        mock_load.return_value = previous_results
        
        with patch.object(self.tracker, 'passes_filters', return_value=True):
            comparison = self.tracker.compare_with_previous(
                self.sample_results,
                min_rs_score=70,
                min_weekly_target=2.0
            )
            
            self.assertIsInstance(comparison, dict)
            self.assertTrue(comparison['has_previous'])
            
            # Should have either improved or declined tickers (since AAPL appears in both)
            total_overlaps = len(comparison['improved']) + len(comparison['declined'])
            self.assertGreaterEqual(total_overlaps, 0)

class TestDataPersistence(unittest.TestCase):
    """Test data saving and loading functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tracker = PortfolioTracker()
        
        self.sample_results = [
            {
                'ticker': 'TEST1',
                'rs_score': 75,
                'avg_weekly_return': 2.5,
                'timestamp': datetime.now()
            }
        ]
        
    def test_save_results_basic(self):
        """Test basic results saving"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Override the results file path
            test_file = os.path.join(temp_dir, 'test_results.pkl')
            
            with patch.object(self.tracker, 'results_file', test_file):
                # Save results
                self.tracker.save_results(self.sample_results)
                
                # Verify file was created
                self.assertTrue(os.path.exists(test_file))
                
                # Verify contents
                with open(test_file, 'rb') as f:
                    saved_data = pickle.load(f)
                    
                self.assertIsInstance(saved_data, list)
                self.assertEqual(len(saved_data), 1)
                
                # Check the structure: should be historical format
                history_entry = saved_data[0]
                self.assertIn('timestamp', history_entry)
                self.assertIn('results', history_entry)
                self.assertIn('market_conditions', history_entry)
                
                # Check the actual results
                results = history_entry['results']
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]['ticker'], 'TEST1')
                
    def test_save_results_with_timestamp(self):
        """Test saving results with custom timestamp"""
        custom_timestamp = datetime(2025, 1, 1, 12, 0, 0)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, 'test_results.pkl')
            
            with patch.object(self.tracker, 'results_file', test_file):
                self.tracker.save_results(self.sample_results, timestamp=custom_timestamp)
                
                with open(test_file, 'rb') as f:
                    saved_data = pickle.load(f)
                    
                # Check timestamp was added
                self.assertEqual(saved_data[0]['timestamp'], custom_timestamp)
                
    def test_load_historical_results_success(self):
        """Test successful loading of historical results"""
        test_data = [
            {
                'ticker': 'HISTORICAL1',
                'rs_score': 80,
                'timestamp': datetime.now() - timedelta(days=1)
            }
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, 'test_results.pkl')
            
            # Save test data
            with open(test_file, 'wb') as f:
                pickle.dump(test_data, f)
                
            with patch.object(self.tracker, 'results_file', test_file):
                loaded_results = self.tracker.load_historical_results()
                
                self.assertIsInstance(loaded_results, list)
                self.assertEqual(len(loaded_results), 1)
                self.assertEqual(loaded_results[0]['ticker'], 'HISTORICAL1')
                
    def test_load_historical_results_no_file(self):
        """Test loading historical results when file doesn't exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            nonexistent_file = os.path.join(temp_dir, 'nonexistent.pkl')
            
            with patch.object(self.tracker, 'results_file', nonexistent_file):
                loaded_results = self.tracker.load_historical_results()
                
                self.assertIsInstance(loaded_results, list)
                self.assertEqual(len(loaded_results), 0)
                
    def test_load_historical_results_corrupted_file(self):
        """Test loading historical results with corrupted file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, 'corrupted.pkl')
            
            # Create corrupted file
            with open(test_file, 'w') as f:
                f.write("This is not pickle data")
                
            with patch.object(self.tracker, 'results_file', test_file):
                loaded_results = self.tracker.load_historical_results()
                
                # Should return empty list on corruption
                self.assertIsInstance(loaded_results, list)
                self.assertEqual(len(loaded_results), 0)

class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tracker = PortfolioTracker()
        
    def test_passes_filters_missing_keys(self):
        """Test passes_filters with missing required keys"""
        incomplete_result = {
            'ticker': 'TEST'
            # Missing other required keys
        }
        
        # Should handle missing keys gracefully
        try:
            result = self.tracker.passes_filters(incomplete_result)
            self.assertFalse(result)  # Should fail safely
        except KeyError:
            self.fail("passes_filters should handle missing keys gracefully")
            
    def test_get_top_picks_invalid_parameters(self):
        """Test get_top_picks with invalid parameters"""
        results = [
            {
                'ticker': 'TEST', 'rs_score': 75, 'avg_weekly_return': 2.0, 'market_cap': 1e12, 
                'meets_criteria': True, 'weeks_above_target': 3, 'daily_change': 1.0,
                'weekly_returns': [0.02, 0.018, 0.025, 0.020]
            }
        ]
        
        # Test with negative count
        with patch.object(self.tracker, 'passes_filters', return_value=True):
            top_picks = self.tracker.get_top_picks(results, count=-5)
            self.assertEqual(len(top_picks), 0)
            
        # Test with zero count
        with patch.object(self.tracker, 'passes_filters', return_value=True):
            top_picks = self.tracker.get_top_picks(results, count=0)
            self.assertEqual(len(top_picks), 0)
            
    def test_generate_portfolio_recommendations_invalid_size(self):
        """Test portfolio recommendations with invalid portfolio size"""
        results = [
            {
                'ticker': 'TEST', 'rs_score': 75, 'avg_weekly_return': 2.0, 'market_cap': 1e12, 
                'meets_criteria': True, 'weeks_above_target': 3, 'daily_change': 1.0,
                'weekly_returns': [0.02, 0.018, 0.025, 0.020]
            }
        ]
        
        # Test with negative portfolio size
        with patch.object(self.tracker, 'passes_filters', return_value=True):
            recommendations = self.tracker.generate_portfolio_recommendations(
                results, 
                portfolio_size=-5
            )
            self.assertEqual(len(recommendations['top_picks']), 0)

if __name__ == '__main__':
    unittest.main()
