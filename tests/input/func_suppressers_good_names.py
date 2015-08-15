"""
Check for django specific variable names
"""
import logging

logger = logging.getLogger(__name__)

urlpatterns = []

foobar = 0  # added to check that bad names are checked also
