# This is instrument registry service which keeps track of all the tradable instruments.

### Desired Architecture

instrument_registry_project/
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── .env                            # Development environment file
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile.dev
├── Dockerfile.test
├── Dockerfile.prod
├── docker-compose.dev.yml
├── docker-compose.test.yml
├── docker-compose.prod.yml
├── Makefile
├── setup.py                        # Build configuration for sdist
├── pyproject.toml
├── manage.py                       # Enhanced management script
├── celery_app.py                   # Celery configuration
│
├── instruments/                    # Main application package (all Python code)
│   ├── __init__.py
│   │
│   ├── app/                        # App factory and registration (NEW)
│   │   ├── __init__.py
│   │   ├── factory.py              # App factory (moved from app.py)
│   │   ├── blueprints.py           # Blueprint registration
│   │   ├── error_handlers.py       # Error handlers registration
│   │   └── extensions.py           # Extensions initialization
│   │
│   ├── config/                     # Configuration management (NEW)
│   │   ├── __init__.py
│   │   ├── base.py                 # Base configuration class
│   │   ├── development.py          # Development configuration
│   │   ├── testing.py              # Testing configuration
│   │   ├── production.py           # Production configuration
│   │   └── settings.py             # Settings loader/manager
│   │
│   ├── apps/                       # Application modules
│   │   ├── __init__.py
│   │   └── api/                    # API modules
│   │       ├── __init__.py
│   │       └── v1/                 # API version 1
│   │           ├── __init__.py
│   │           ├── instruments/    # Instruments blueprint
│   │           │   ├── __init__.py
│   │           │   ├── routes.py   # URL routing
│   │           │   ├── views.py    # API views/controllers
│   │           │   ├── services.py # Business logic services
│   │           │   ├── models.py   # API-specific models
│   │           │   └── schemas.py  # Pydantic validation schemas
│   │           │
│   │           ├── admin/          # Admin blueprint
│   │           │   ├── __init__.py
│   │           │   ├── routes.py
│   │           │   ├── views.py
│   │           │   ├── services.py
│   │           │   ├── models.py
│   │           │   └── schemas.py
│   │           │
│   │           ├── health/         # Health check blueprint
│   │           │   ├── __init__.py
│   │           │   ├── routes.py
│   │           │   ├── views.py
│   │           │   ├── models.py
│   │           │   └── schemas.py
│   │           │
│   │           └── analytics/      # Analytics blueprint
│   │               ├── __init__.py
│   │               ├── routes.py
│   │               ├── views.py
│   │               ├── services.py
│   │               ├── models.py
│   │               └── schemas.py
│   │
│   ├── database/                   # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── base_models.py
│   │   ├── repositories.py
│   │   └── migrations/
│   │       ├── __init__.py
│   │       ├── alembic.ini
│   │       ├── env.py
│   │       └── versions/
│   │
│   ├── cache/                      # Caching layer
│   │   ├── __init__.py
│   │   ├── redis_client.py
│   │   ├── cache_manager.py
│   │   └── serializers.py
│   │
│   ├── schemas/                    # Common/shared schemas
│   │   ├── __init__.py
│   │   ├── common_schemas.py
│   │   └── base_schemas.py
│   │
│   ├── utils/                      # Utility modules
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── rate_limiter.py
│   │   ├── validators.py
│   │   ├── decorators.py
│   │   ├── exceptions.py
│   │   ├── helpers.py
│   │   ├── constants.py
│   │   └── auth_utils.py
│   │
│   ├── tasks/                      # Background tasks
│   │   ├── __init__.py
│   │   ├── celery_tasks.py
│   │   ├── data_import.py
│   │   ├── data_export.py
│   │   └── maintenance.py
│   │
│   ├── monitoring/                 # Monitoring and observability
│   │   ├── __init__.py
│   │   ├── sentry_config.py
│   │   ├── metrics.py
│   │   ├── tracing.py
│   │   └── alerts.py
│   │
│   ├── middleware/                 # Custom middleware
│   │   ├── __init__.py
│   │   ├── gateway_auth.py
│   │   ├── user_context.py
│   │   ├── auth_decorators.py
│   │   ├── cors.py
│   │   ├── rate_limiting.py
│   │   ├── request_id.py
│   │   └── security.py
│   │
│   └── management/                 # Management commands
│       ├── __init__.py
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── server.py
│       │   ├── database.py
│       │   ├── cache.py
│       │   ├── testing.py
│       │   ├── deployment.py
│       │   ├── maintenance.py
│       │   ├── monitoring.py
│       │   └── development.py
│       ├── base.py
│       └── registry.py
│
├── tests/                          # Test suite (mirrors instruments structure)
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration
│   ├── fixtures/                   # Test fixtures
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── cache.py
│   │   └── sample_data.py
│   │
│   ├── app/                        # App factory tests (NEW)
│   │   ├── __init__.py
│   │   ├── test_factory.py
│   │   ├── test_blueprints.py
│   │   ├── test_error_handlers.py
│   │   └── test_extensions.py
│   │
│   ├── config/                     # Configuration tests (NEW)
│   │   ├── __init__.py
│   │   ├── test_base.py
│   │   ├── test_development.py
│   │   ├── test_testing.py
│   │   ├── test_production.py
│   │   └── test_settings.py
│   │
│   ├── apps/                       # Mirror apps structure
│   │   ├── __init__.py
│   │   └── api/
│   │       ├── __init__.py
│   │       └── v1/
│   │           ├── __init__.py
│   │           ├── instruments/    # Instruments blueprint tests
│   │           │   ├── __init__.py
│   │           │   ├── test_routes.py
│   │           │   ├── test_views.py
│   │           │   ├── test_services.py
│   │           │   ├── test_models.py
│   │           │   └── test_schemas.py
│   │           │
│   │           ├── admin/          # Admin blueprint tests
│   │           │   ├── __init__.py
│   │           │   ├── test_routes.py
│   │           │   ├── test_views.py
│   │           │   ├── test_services.py
│   │           │   ├── test_models.py
│   │           │   └── test_schemas.py
│   │           │
│   │           ├── health/         # Health blueprint tests
│   │           │   ├── __init__.py
│   │           │   ├── test_routes.py
│   │           │   ├── test_views.py
│   │           │   ├── test_models.py
│   │           │   └── test_schemas.py
│   │           │
│   │           └── analytics/      # Analytics blueprint tests
│   │               ├── __init__.py
│   │               ├── test_routes.py
│   │               ├── test_views.py
│   │               ├── test_services.py
│   │               ├── test_models.py
│   │               └── test_schemas.py
│   │
│   ├── database/                   # Database tests
│   │   ├── __init__.py
│   │   ├── test_connection.py
│   │   ├── test_base_models.py
│   │   └── test_repositories.py
│   │
│   ├── cache/                      # Cache tests
│   │   ├── __init__.py
│   │   ├── test_redis_client.py
│   │   ├── test_cache_manager.py
│   │   └── test_serializers.py
│   │
│   ├── utils/                      # Utility tests
│   │   ├── __init__.py
│   │   ├── test_logger.py
│   │   ├── test_rate_limiter.py
│   │   ├── test_validators.py
│   │   ├── test_decorators.py
│   │   ├── test_exceptions.py
│   │   ├── test_helpers.py
│   │   └── test_auth_utils.py
│   │
│   ├── tasks/                      # Background task tests
│   │   ├── __init__.py
│   │   ├── test_celery_tasks.py
│   │   ├── test_data_import.py
│   │   ├── test_data_export.py
│   │   └── test_maintenance.py
│   │
│   ├── monitoring/                 # Monitoring tests
│   │   ├── __init__.py
│   │   ├── test_sentry_config.py
│   │   ├── test_metrics.py
│   │   └── test_tracing.py
│   │
│   ├── middleware/                 # Middleware tests
│   │   ├── __init__.py
│   │   ├── test_gateway_auth.py
│   │   ├── test_user_context.py
│   │   ├── test_auth_decorators.py
│   │   ├── test_cors.py
│   │   ├── test_rate_limiting.py
│   │   ├── test_request_id.py
│   │   └── test_security.py
│   │
│   ├── management/                 # Management command tests
│   │   ├── __init__.py
│   │   ├── test_base.py
│   │   ├── test_registry.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       ├── test_server.py
│   │       ├── test_database.py
│   │       ├── test_cache.py
│   │       ├── test_testing.py
│   │       ├── test_deployment.py
│   │       ├── test_maintenance.py
│   │       ├── test_monitoring.py
│   │       └── test_development.py
│   │
│   ├── unit/                       # Unit tests (cross-cutting)
│   │   ├── __init__.py
│   │   ├── test_app.py
│   │   ├── test_config.py
│   │   └── test_integration_points.py
│   │
│   ├── integration/                # Integration tests
│   │   ├── __init__.py
│   │   ├── test_api_endpoints.py
│   │   ├── test_database_integration.py
│   │   ├── test_cache_integration.py
│   │   ├── test_background_tasks.py
│   │   └── test_gateway_auth_integration.py
│   │
│   ├── functional/                 # Functional tests
│   │   ├── __init__.py
│   │   ├── test_instrument_workflow.py
│   │   ├── test_trading_data_workflow.py
│   │   ├── test_analytics_workflow.py
│   │   └── test_admin_workflow.py
│   │
│   ├── performance/                # Performance tests
│   │   ├── __init__.py
│   │   ├── test_api_performance.py
│   │   ├── test_database_performance.py
│   │   ├── test_cache_performance.py
│   │   └── test_load_testing.py
│   │
│   ├── performance_test/           # Additional performance testing
│   │   ├── __init__.py
│   │   ├── stress_tests.py
│   │   ├── benchmark_tests.py
│   │   ├── scalability_tests.py
│   │   └── endurance_tests.py
│   │
│   └── business_test/              # Business logic tests
│       ├── __init__.py
│       ├── test_business_rules.py
│       ├── test_workflows.py
│       ├── test_data_validation.py
│       ├── test_compliance.py
│       └── test_domain_logic.py
│
├── scripts/                        # All shell scripts
│   ├── entry_point_dev.sh          # Development entry point
│   ├── entry_point_test.sh         # Test entry point
│   ├── entry_point_prod.sh         # Production entry point
│   ├── init_db.sh                  # Database initialization script
│   ├── seed_data.sh                # Sample data seeding script
│   ├── migrate_data.sh             # Data migration script
│   ├── backup_db.sh                # Database backup script
│   ├── restore_db.sh               # Database restore script
│   ├── setup_test_env.sh           # Test environment setup
│   ├── cleanup_test_env.sh         # Test environment cleanup
│   ├── run_tests.sh                # Test runner script
│   ├── deploy_dev.sh               # Development deployment
│   ├── deploy_staging.sh           # Staging deployment
│   ├── deploy_prod.sh              # Production deployment
│   ├── rollback.sh                 # Rollback script
│   ├── health_check.sh             # Health check script
│   └── backup.sh                   # Backup script
│
├── deployment/                     # Deployment configurations (infrastructure only)
│   ├── kubernetes/                 # Kubernetes manifests
│   │   ├── dev/
│   │   │   ├── namespace.yaml
│   │   │   ├── configmap.yaml
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   ├── staging/
│   │   │   ├── namespace.yaml
│   │   │   ├── configmap.yaml
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   └── prod/
│   │       ├── namespace.yaml
│   │       ├── configmap.yaml
│   │       ├── secret.yaml
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── ingress.yaml
│   │       ├── hpa.yaml
│   │       └── pdb.yaml
│   │
│   ├── helm/                       # Helm charts
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   ├── values-dev.yaml
│   │   ├── values-staging.yaml
│   │   ├── values-prod.yaml
│   │   └── templates/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── configmap.yaml
│   │       ├── secret.yaml
│   │       └── ingress.yaml
│   │
│   └── terraform/                  # Infrastructure as code
│       ├── environments/
│       │   ├── dev/
│       │   ├── staging/
│       │   └── prod/
│       ├── modules/
│       │   ├── database/
│       │   ├── redis/
│       │   └── kubernetes/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── providers.tf
│
├── docs/                           # Documentation
│   ├── README.md
│   ├── API.md
│   ├── DEPLOYMENT.md
│   ├── DEVELOPMENT.md
│   ├── ARCHITECTURE.md
│   ├── AUTHENTICATION.md
│   ├── TROUBLESHOOTING.md
│   ├── TESTING.md
│   ├── MANAGEMENT_COMMANDS.md
│   └── openapi/
│
├── logs/                           # Log files (gitignored)
│   └── .gitkeep
│
├── uploads/                        # File uploads (gitignored)
│   └── .gitkeep
│
├── static/                         # Static files
│   ├── css/
│   ├── js/
│   └── images/
│
└── templates/                      # Jinja2 templates (if needed)
    ├── base.html
    └── admin/
