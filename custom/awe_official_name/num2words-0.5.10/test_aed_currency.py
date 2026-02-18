#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script to verify AED currency implementation across different languages
"""

from num2words import num2words

def test_aed_currency():
    """Test AED currency conversion in various languages"""
    
    # Test English
    print("English:")
    print("1.00 AED:", num2words(1.00, lang='en', to='currency', currency='AED'))
    print("2.00 AED:", num2words(2.00, lang='en', to='currency', currency='AED'))
    print("10.50 AED:", num2words(10.50, lang='en', to='currency', currency='AED'))
    print("0.50 AED:", num2words(0.50, lang='en', to='currency', currency='AED'))
    print()
    
    # Test Arabic
    print("Arabic:")
    print("1.00 AED:", num2words(1.00, lang='ar', to='currency', currency='AED'))
    print("2.00 AED:", num2words(2.00, lang='ar', to='currency', currency='AED'))
    print("10.50 AED:", num2words(10.50, lang='ar', to='currency', currency='AED'))
    print("0.50 AED:", num2words(0.50, lang='ar', to='currency', currency='AED'))
    print()
    
    # Test Portuguese
    print("Portuguese:")
    print("1.00 AED:", num2words(1.00, lang='pt', to='currency', currency='AED'))
    print("2.00 AED:", num2words(2.00, lang='pt', to='currency', currency='AED'))
    print("10.50 AED:", num2words(10.50, lang='pt', to='currency', currency='AED'))
    print("0.50 AED:", num2words(0.50, lang='pt', to='currency', currency='AED'))
    print()
    
    # Test Spanish
    print("Spanish:")
    print("1.00 AED:", num2words(1.00, lang='es', to='currency', currency='AED'))
    print("2.00 AED:", num2words(2.00, lang='es', to='currency', currency='AED'))
    print("10.50 AED:", num2words(10.50, lang='es', to='currency', currency='AED'))
    print("0.50 AED:", num2words(0.50, lang='es', to='currency', currency='AED'))
    print()
    
    # Test German
    print("German:")
    print("1.00 AED:", num2words(1.00, lang='de', to='currency', currency='AED'))
    print("2.00 AED:", num2words(2.00, lang='de', to='currency', currency='AED'))
    print("10.50 AED:", num2words(10.50, lang='de', to='currency', currency='AED'))
    print("0.50 AED:", num2words(0.50, lang='de', to='currency', currency='AED'))
    print()
    
    # Test French
    print("French:")
    print("1.00 AED:", num2words(1.00, lang='fr', to='currency', currency='AED'))
    print("2.00 AED:", num2words(2.00, lang='fr', to='currency', currency='AED'))
    print("10.50 AED:", num2words(10.50, lang='fr', to='currency', currency='AED'))
    print("0.50 AED:", num2words(0.50, lang='fr', to='currency', currency='AED'))
    print()
    
    # Test Dutch
    print("Dutch:")
    print("1.00 AED:", num2words(1.00, lang='nl', to='currency', currency='AED'))
    print("2.00 AED:", num2words(2.00, lang='nl', to='currency', currency='AED'))
    print("10.50 AED:", num2words(10.50, lang='nl', to='currency', currency='AED'))
    print("0.50 AED:", num2words(0.50, lang='nl', to='currency', currency='AED'))

if __name__ == "__main__":
    test_aed_currency()