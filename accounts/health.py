from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.core.cache import cache
import time

class HealthCheckView(APIView):
    """
    Health check endpoint for monitoring and load balancers
    Returns system status and component health
    """
    permission_classes = []  # Public endpoint
    
    def get(self, request):
        """
        Comprehensive health check
        Returns 200 if all systems operational, 503 if any critical system is down
        """
        health_status = {
            'status': 'healthy',
            'timestamp': int(time.time()),
            'checks': {}
        }
        
        overall_healthy = True
        
        # Database check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            health_status['checks']['database'] = {
                'status': 'healthy',
                'message': 'Database connection successful'
            }
        except Exception as e:
            health_status['checks']['database'] = {
                'status': 'unhealthy',
                'message': f'Database error: {str(e)}'
            }
            overall_healthy = False
        
        # Cache check (optional - comment out if not using cache)
        try:
            cache_key = 'health_check_test'
            cache.set(cache_key, 'test', 10)
            cache_value = cache.get(cache_key)
            if cache_value == 'test':
                health_status['checks']['cache'] = {
                    'status': 'healthy',
                    'message': 'Cache operational'
                }
            else:
                health_status['checks']['cache'] = {
                    'status': 'degraded',
                    'message': 'Cache not storing values correctly'
                }
        except Exception as e:
            health_status['checks']['cache'] = {
                'status': 'unavailable',
                'message': f'Cache error: {str(e)}'
            }
            # Cache failures are not critical
        
        # Application check
        health_status['checks']['application'] = {
            'status': 'healthy',
            'message': 'Application running',
            'version': '1.0.0'
        }
        
        # Set overall status
        if not overall_healthy:
            health_status['status'] = 'unhealthy'
            return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response(health_status, status=status.HTTP_200_OK)


class ReadinessCheckView(APIView):
    """
    Readiness check - indicates if app is ready to serve traffic
    Used by Kubernetes and other orchestrators
    """
    permission_classes = []
    
    def get(self, request):
        """
        Quick readiness check
        Returns 200 if ready, 503 if not ready
        """
        try:
            # Quick database check
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            return Response({
                'status': 'ready',
                'timestamp': int(time.time())
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'not_ready',
                'error': str(e),
                'timestamp': int(time.time())
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class LivenessCheckView(APIView):
    """
    Liveness check - indicates if app is alive
    Used by Kubernetes and other orchestrators
    """
    permission_classes = []
    
    def get(self, request):
        """
        Simple liveness check
        Always returns 200 unless the app is completely dead
        """
        return Response({
            'status': 'alive',
            'timestamp': int(time.time())
        }, status=status.HTTP_200_OK)
