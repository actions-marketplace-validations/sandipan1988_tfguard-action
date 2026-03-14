#!/usr/bin/env python3
import sys
import os
import zipfile
import io
import json
import urllib.request
import urllib.error
import argparse

def create_multipart_payload(zip_bytes, filename, boundary):
    # Construct standard multipart/form-data payload
    parts = []
    
    # Add files field
    parts.append(f"--{boundary}".encode('utf-8'))
    parts.append(f'Content-Disposition: form-data; name="files"; filename="{filename}"'.encode('utf-8'))
    parts.append(b'Content-Type: application/zip')
    parts.append(b'')
    parts.append(zip_bytes)
    
    parts.append(f"--{boundary}--".encode('utf-8'))
    parts.append(b'')
    
    return b'\r\n'.join(parts)

def main():
    parser = argparse.ArgumentParser(description='TFGuard GitHub Action Runner')
    parser.add_argument('--target-dir', default='.', help='Directory with Terraform files')
    parser.add_argument('--fail-on-critical', default='true', help='Fail on CRITICAL')
    parser.add_argument('--fail-on-high', default='false', help='Fail on HIGH')
    parser.add_argument('--fail-on-medium', default='false', help='Fail on MEDIUM')
    parser.add_argument('--fail-on-low', default='false', help='Fail on LOW')
    parser.add_argument('--api-url', default='https://tfgaurd.com/api/check-files', help='API URL')
    parser.add_argument('--api-key', default='', help='API Key for paid users')
    
    args = parser.parse_args()
    
    fail_thresholds = {
        'CRITICAL': args.fail_on_critical.lower() == 'true',
        'HIGH': args.fail_on_high.lower() == 'true',
        'MEDIUM': args.fail_on_medium.lower() == 'true',
        'LOW': args.fail_on_low.lower() == 'true',
    }
    
    print(f"::group::🔍 Preparing TFGuard Scan")
    print(f"Target directory: {args.target_dir}")
    print(f"API Endpiont: {args.api_url}")
    
    # 1. Collect .tf files
    tf_files = []
    for root, dirs, files in os.walk(args.target_dir):
        # Skip common directories to ignore
        dirs[:] = [d for d in dirs if d not in ['.terraform', '.git', 'node_modules']]
        
        for file in files:
            if file.endswith('.tf'):
                full_path = os.path.join(root, file)
                # Store relative path for cleaner ZIP and UI output
                rel_path = os.path.relpath(full_path, args.target_dir)
                tf_files.append((full_path, rel_path))
                
    if not tf_files:
        print("No .tf files found in the specified directory.")
        print("::endgroup::")
        sys.exit(0)
        
    print(f"Found {len(tf_files)} Terraform files to scan.")
    
    # 2. Add to ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
        for full_path, rel_path in tf_files:
            zf.write(full_path, arcname=rel_path)
    
    zip_bytes = zip_buffer.getvalue()
    
    # 3. Create Request
    boundary = "TFGuardBoundary1234567890"
    payload = create_multipart_payload(zip_bytes, "terraform_files.zip", boundary)
    
    req = urllib.request.Request(args.api_url, data=payload, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("User-Agent", "TFGuard-GitHub-Action/1.0")
    
    if args.api_key:
        # Support both 'key' and 'Bearer key' formats
        auth_value = args.api_key if args.api_key.startswith('Bearer ') else f"Bearer {args.api_key}"
        req.add_header("Authorization", auth_value)
        print("Using API Key for authenticated request...")
    else:
        print("No API Key provided, using free tier...")
    
    print("Sending files to TFGuard API...")
    print("::endgroup::")
    
    # 4. Execute Request
    status_code = 500
    response_data = {}
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_data = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        status_code = e.code
        try:
            response_data = json.loads(e.read().decode('utf-8'))
        except:
            response_data = {"error": f"HTTP {status_code}: {e.reason}"}
    except Exception as e:
        print(f"::error::Failed to connect to TFGuard API: {str(e)}")
        sys.exit(1)
        
    # 5. Process Response
    if status_code not in (200, 201):
        err = response_data.get('error', 'Unknown Error')
        print(f"::error::API Error: {err}")
        sys.exit(1)
        
    passed = response_data.get('passed', False)
    counts = response_data.get('severity_counts', {})
    
    print("::group::📊 TFGuard Scan Results")
    print(f"Total Resources Scanned: {response_data.get('total_resource_count', 0)}")
    print(f"Total Violations: {response_data.get('total_violation_count', 0)}")
    
    # Display counts
    for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        if counts.get(sev, 0) > 0:
            print(f"  {sev}: {counts[sev]}")
    print("::endgroup::")
    
    # Print individual violations
    fail_pipeline = False
    
    for file_summary in response_data.get('files', []):
        filename = file_summary.get('filename')
        violations = file_summary.get('violations', [])
        
        if not violations:
            continue
            
        print(f"\n📁 File: {filename}")
        for idx, v in enumerate(violations, 1):
            severity = v.get('severity', 'UNKNOWN').upper()
            rule = v.get('rule', '')
            violation_msg = v.get('violation', '')
            res_type = v.get('resource_type', '')
            res_name = v.get('resource_name', '')
            
            # Format Github Actions output based on severity
            prefix = "::warning"
            if fail_thresholds.get(severity, False):
                prefix = "::error"
                fail_pipeline = True
                
            print(f"{prefix} title=TFGuard: {severity} [{rule}]::File: {filename} - Resource: {res_type}.{res_name} - {violation_msg}")
            
    print("\n=======================================================")
    if not fail_pipeline:
        print("✅ Terraform Security Check Passed (Or within thresholds)")
        sys.exit(0)
    else:
        print("❌ Terraform Security Check Failed (Threshold exceeded)")
        sys.exit(1)

if __name__ == "__main__":
    main()
