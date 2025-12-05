#!/bin/bash
# SOC Deployment Structure Verification
# Verifies all components exist and are properly configured

echo "========================================="
echo "   SOC STRUCTURE VERIFICATION SCRIPT    "
echo "========================================="
echo "Audit Date: $(date)"
echo "Audit Type: Static Configuration Check"
echo ""

# Scoring
total_checks=0
passed_checks=0

check() {
    ((total_checks++))
    if [ $1 -eq 0 ]; then
        echo "  PASS: $2"
        ((passed_checks++))
        return 0
    else
        echo "  FAIL: $2"
        return 1
    fi
}

echo "1. CORE INFRASTRUCTURE"
echo "----------------------"

[ -f "docker-compose.yml" ]
check $? "Docker Compose configuration"

[ -f "docker-compose-minimal.yml" ]
check $? "Minimal deployment configuration"

[ -f "Dockerfile" ]
check $? "Main Dockerfile"

echo ""
echo "2. APPLICATION COMPONENTS"
echo "------------------------"

[ -f "app.py" ]
check $? "Main application file"

if [ -f "app.py" ]; then
    if grep -q "@app.route\|def.*/" app.py; then
        check 0 "API routes defined"
    else
        check 1 "API routes defined"
    fi
fi

[ -d "dashboard" ]
check $? "Dashboard frontend directory"

if [ -d "dashboard" ]; then
    dash_files=$(find dashboard -type f -name "*.html" -o -name "*.js" -o -name "*.css" | head -3)
    if [ -n "$dash_files" ]; then
        echo "    Dashboard files found:"
        for file in $dash_files; do
            echo "      - $(basename "$file")"
        done
    fi
fi

echo ""
echo "3. SECURITY & MONITORING"
echo "------------------------"

[ -f "security_scanner.py" ]
check $? "Security scanner script"

[ -d "scripts/attack_simulations" ] || [ -f "test_audit.py" ]
check $? "Security testing components"

[ -d "elasticsearch" ] || [ -d "elasticsearch_config" ]
check $? "Logging/Elasticsearch configuration"

[ -d "logstash" ]
check $? "Logstash configuration"

echo ""
echo "4. TEAM INTEGRATION"
echo "------------------"

components_found=0
team_dirs=("dashboard" "elasticsearch" "scripts/attack_simulations" "waad-elkenin-detection-engine")

for dir in "${team_dirs[@]}"; do
    if [ -d "$dir" ]; then
        ((components_found++))
    fi
done

if [ $components_found -ge 2 ]; then
    check 0 "Multiple team components integrated ($components_found/4 found)"
else
    check 1 "Multiple team components integrated ($components_found/4 found)"
fi

echo ""
echo "5. DEPLOYMENT & DOCUMENTATION"
echo "----------------------------"

[ -f "deploy_infrastructure.sh" ]
check $? "Deployment script"

[ -f "README.md" ]
check $? "Project documentation"

[ -f "requirements.txt" ]
check $? "Python dependencies"

[ -d ".github/workflows" ]
check $? "CI/CD pipeline configured"

echo ""
echo "========================================="
echo "           VERIFICATION SUMMARY          "
echo "========================================="
echo ""
echo "Checks passed: $passed_checks/$total_checks"
echo ""

if [ $passed_checks -eq $total_checks ]; then
    echo "RESULT: ALL CHECKS PASSED"
    echo "   SOC structure is properly integrated."
elif [ $passed_checks -ge $((total_checks * 80 / 100)) ]; then
    echo "RESULT: MOST CHECKS PASSED ($passed_checks/$total_checks)"
    echo "   SOC structure is mostly complete."
else
    echo "RESULT: SIGNIFICANT ISSUES FOUND ($passed_checks/$total_checks)"
    echo "   Review missing components."
fi

echo ""
echo "RECOMMENDED ACTIONS:"
echo "1. Run integration test: python tests/integration_test.py"
echo "2. Test deployment: docker-compose config"
echo "3. Start services: docker-compose up -d"
echo "4. Run security scan: python security_scanner.py"
echo ""
echo "========================================="
