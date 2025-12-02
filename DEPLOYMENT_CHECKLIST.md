# Deployment Checklist - Invite-Only Website

## Pre-Deployment Steps

### 1. Environment Configuration ☐
- [ ] Copy `.env.example` to `.env`
- [ ] Set `POSTGRES_PASSWORD` to a strong password (20+ characters)
- [ ] Set `SESSION_SECRET` to a random string (32+ characters)
- [ ] Configure `BASE_URL` to your actual domain
- [ ] Set `OPENAI_API_KEY` if using OpenAI models
- [ ] Configure Discord integration (optional)

### 2. SSL/TLS Certificates ☐
- [ ] Generate SSL certificate (Let's Encrypt or self-signed)
- [ ] Copy certificate to `./ssl/cert.pem`
- [ ] Copy private key to `./ssl/key.pem`
- [ ] Update `nginx.conf` to enable HTTPS server block
- [ ] Test certificate validity: `openssl x509 -in ssl/cert.pem -text -noout`

### 3. Security Configuration ☐
- [ ] Review and update firewall rules
- [ ] Enable only necessary ports (80, 443, 22)
- [ ] Configure fail2ban for SSH protection
- [ ] Set up automated security updates
- [ ] Review `SECURITY_SUMMARY.md`

### 4. Database Preparation ☐
- [ ] Review `init-db.sql` schema
- [ ] Plan database backup strategy
- [ ] Configure database connection pool size
- [ ] Test database connectivity

## Deployment Steps

### Step 1: Clone and Configure
```bash
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-
cp .env.example .env
nano .env  # Configure your settings
```

### Step 2: Build and Start Services
```bash
# Build containers
docker-compose build

# Start services
docker-compose up -d

# Check service status
docker-compose ps
```

### Step 3: Verify Services
```bash
# Check web app logs
docker-compose logs -f web-app

# Check database is ready
docker-compose logs postgres | grep "ready to accept connections"

# Test health endpoint
curl http://localhost:8090/health
```

### Step 4: Initial Admin Setup
1. Open browser to `http://localhost:8090` (or your domain)
2. Login with default credentials:
   - Email: `admin@localhost`
   - Password: `admin123`
3. **IMMEDIATELY** change the admin password:
   ```bash
   docker-compose exec postgres psql -U postgres strategickhaos
   # Update password to new hash
   ```

### Step 5: Generate First Invites
1. Login as admin
2. Navigate to "Invitations" section
3. Generate invite code for first user
4. Send invite URL to user

## Post-Deployment Verification

### Functionality Tests ☐
- [ ] Admin can login successfully
- [ ] Admin can generate invite codes
- [ ] User can register with valid invite code
- [ ] User can login after registration
- [ ] Chat interface loads correctly
- [ ] LLM responds to messages
- [ ] Conversation history is saved
- [ ] Rate limiting works (test with curl)
- [ ] Session expires after 24 hours
- [ ] Logout works correctly

### Security Tests ☐
- [ ] HTTPS redirect works (if enabled)
- [ ] SSL certificate is valid
- [ ] Security headers are present (check with browser dev tools)
- [ ] Rate limiting triggers after 100 requests
- [ ] Authentication required for protected routes
- [ ] CSRF protection blocks cross-origin requests
- [ ] SQL injection attempts fail
- [ ] XSS attempts are blocked
- [ ] Session cookies have correct flags (httpOnly, secure, SameSite)

### Performance Tests ☐
- [ ] Page load time < 2 seconds
- [ ] API response time < 500ms (95th percentile)
- [ ] Database connection pool adequate
- [ ] No memory leaks after 24 hours
- [ ] LLM requests complete within 30 seconds

## Monitoring Setup

### Grafana Dashboard ☐
1. Access Grafana at `http://localhost:3000/monitoring/`
2. Login with default credentials (admin/admin)
3. Change admin password
4. Import provided dashboards (if available)
5. Configure alerts for:
   - [ ] High error rate (>5% of requests)
   - [ ] Slow response time (>2s)
   - [ ] Database connection errors
   - [ ] High CPU usage (>80%)
   - [ ] High memory usage (>80%)

### Log Monitoring ☐
- [ ] Configure log rotation
- [ ] Set up log aggregation (optional)
- [ ] Test audit log entries are being created
- [ ] Configure log alerts for security events

## Backup Configuration

### Database Backups ☐
```bash
# Create backup directory
mkdir -p /var/backups/sovereignty-db

# Create backup script
cat > /usr/local/bin/backup-sovereignty-db.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="/var/backups/sovereignty-db/backup_${DATE}.sql"
docker-compose exec -T postgres pg_dump -U postgres strategickhaos > "$BACKUP_FILE"
gzip "$BACKUP_FILE"
# Keep only last 30 days
find /var/backups/sovereignty-db -name "*.sql.gz" -mtime +30 -delete
EOF

chmod +x /usr/local/bin/backup-sovereignty-db.sh

# Add to cron (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-sovereignty-db.sh") | crontab -
```

### Application Backups ☐
- [ ] Backup `.env` file (securely)
- [ ] Backup SSL certificates
- [ ] Backup `docker-compose.yml` configuration
- [ ] Document custom configuration changes

## Maintenance Plan

### Daily ☐
- [ ] Review audit logs for suspicious activity
- [ ] Check application health dashboard
- [ ] Verify backups completed successfully

### Weekly ☐
- [ ] Run `npm audit` for dependency vulnerabilities
- [ ] Review user registration patterns
- [ ] Check disk space usage
- [ ] Review rate limiting logs

### Monthly ☐
- [ ] Update dependencies (`npm update`)
- [ ] Security audit with `npm audit fix`
- [ ] Review and rotate logs
- [ ] Test backup restoration
- [ ] Review user access levels
- [ ] Update SSL certificate (if needed)

## Troubleshooting

### Common Issues

**Issue: Web app won't start**
```bash
# Check logs
docker-compose logs web-app

# Common causes:
# 1. Database not ready - wait 30 seconds and retry
# 2. Port 8090 in use - change WEB_PORT in .env
# 3. Missing dependencies - rebuild: docker-compose build web-app
```

**Issue: Cannot login**
```bash
# Reset admin password
docker-compose exec postgres psql -U postgres strategickhaos
UPDATE users SET password_hash = '$2b$10$rKvVPGYEqKN5xqKqZLR4ReJ9H.h2FXqKuHYzqLZoJqLqKtZLLLLLe' 
WHERE email = 'admin@localhost';
# Password is now 'admin123' - change it immediately
```

**Issue: LLM not responding**
```bash
# Check Refinory service
docker-compose ps refinory-api
docker-compose logs refinory-api

# Restart if needed
docker-compose restart refinory-api
```

**Issue: Rate limiting too aggressive**
```bash
# Temporarily adjust in src/config/constants.ts
RATE_LIMIT_MAX_REQUESTS: 200  # Increase from 100

# Rebuild and restart
docker-compose build web-app
docker-compose restart web-app
```

## Rollback Plan

### If Deployment Fails
```bash
# Stop services
docker-compose down

# Restore from backup
docker-compose up -d postgres
docker-compose exec -T postgres psql -U postgres strategickhaos < backup.sql

# Check logs
docker-compose logs
```

### If Security Issue Discovered
```bash
# Immediately revoke all sessions
docker-compose exec postgres psql -U postgres strategickhaos \
  -c "DELETE FROM user_sessions;"

# Take services offline
docker-compose stop web-app

# Investigate and fix
# Redeploy with fix
docker-compose build web-app
docker-compose up -d web-app
```

## Production Hardening

### Additional Security Measures ☐
- [ ] Enable AppArmor or SELinux
- [ ] Configure intrusion detection (fail2ban)
- [ ] Set up WAF (Web Application Firewall)
- [ ] Enable audit logging at OS level
- [ ] Configure DNSSEC
- [ ] Implement DDoS protection (CloudFlare, etc.)
- [ ] Set up honeypot for attack detection
- [ ] Configure SIEM integration

### Performance Optimization ☐
- [ ] Enable Redis for session storage (multi-instance)
- [ ] Configure CDN for static assets
- [ ] Enable gzip compression in Nginx
- [ ] Optimize database indexes
- [ ] Configure connection pooling
- [ ] Enable HTTP/2 in Nginx
- [ ] Set up database read replicas (if needed)

## Sign-Off

### Deployment Team ☐
- [ ] Deployment completed by: _______________
- [ ] Date: _______________
- [ ] All checks passed: Yes / No
- [ ] Issues encountered: _______________
- [ ] Resolution: _______________

### Stakeholder Approval ☐
- [ ] Technical Lead approval: _______________
- [ ] Security Officer approval: _______________
- [ ] Product Owner approval: _______________

## Support Contacts

- **Technical Issues**: admin@localhost
- **Security Issues**: security@localhost
- **User Support**: support@localhost

---

**Document Version**: 1.0
**Last Updated**: 2024-11-23
**Next Review**: 2024-12-23
