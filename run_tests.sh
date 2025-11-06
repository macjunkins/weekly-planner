#!/bin/bash
# Comprehensive test runner for weekly-planner
# Runs all verification tests and reports results

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         Weekly Planner - Comprehensive Test Suite            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Test 1: Setup Verification
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1: Setup Verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 test_setup.py
test1_result=$?
echo ""

# Test 2: Library Integration
if [ $test1_result -eq 0 ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "TEST 2: Library Integration"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    python3 test_lib.py
    test2_result=$?
    echo ""
else
    echo "⚠️  Skipping library integration test (setup verification failed)"
    test2_result=1
fi

# Summary
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                        Test Summary                           ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

if [ $test1_result -eq 0 ]; then
    echo "✅ Setup Verification: PASSED"
else
    echo "❌ Setup Verification: FAILED"
fi

if [ $test2_result -eq 0 ]; then
    echo "✅ Library Integration: PASSED"
else
    echo "❌ Library Integration: FAILED"
fi

echo ""

# Overall result
if [ $test1_result -eq 0 ] && [ $test2_result -eq 0 ]; then
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║  ✅ ALL TESTS PASSED - Repository is ready for development!  ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    exit 0
else
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║  ❌ SOME TESTS FAILED - Please review errors above           ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    exit 1
fi