# models.py
from django.db import models
from django.core.cache import cache
import json
from django.core.exceptions import ValidationError

class AppSetting(models.Model):
    setting = models.CharField(
        max_length=100, 
        unique=True,  # This ensures database-level uniqueness
        db_index=True,  # Add index for better query performance
        primary_key=True  # Makes the setting field the primary key
    )
    value = models.JSONField()

    class Meta:
        ordering = ['setting']
        verbose_name = 'Application Setting'
        verbose_name_plural = 'Application Settings'
        constraints = [
            # Additional database-level unique constraint
            models.UniqueConstraint(
                fields=['setting'], 
                name='unique_setting'
            )
        ]

    def clean(self):
        """Validate the setting before saving"""
        # Ensure setting name is lowercase and stripped
        self.setting = self.setting.lower().strip()
        
        # Check if setting already exists (case-insensitive)
        existing = AppSetting.objects.filter(
            setting__iexact=self.setting
        ).exclude(pk=self.pk).exists()
        
        if existing:
            raise ValidationError({
                'setting': f'Setting "{self.setting}" already exists.'
            })
    
    @classmethod
    def load_settings(cls):
        """Load all settings into a dictionary"""
        settings_dict = {}
        for setting in cls.objects.all():
            try:
                settings_dict[setting.setting] = setting.value
            except json.JSONDecodeError:
                settings_dict[setting.setting] = None
        return settings_dict

    @classmethod
    def initialize_settings(cls):
        """Initialize settings from settings.py if needed"""
        from django.conf import settings
        
        try:
            # Check if settings need to be initialized
            db_setting_id = cls.objects.filter(
                setting='setting_id'
            ).first()
            
            if not db_setting_id or db_setting_id.value != settings.APP_SETTING_ID:
                # Use transaction to ensure atomic operation
                with transaction.atomic():
                    # Clear existing settings
                    cls.objects.all().delete()
                    
                    # Initialize with default settings
                    default_settings = settings.DEFAULT_APP_SETTINGS
                    for setting, value in default_settings.items():
                        cls.objects.create(
                            setting=setting.lower().strip(),
                            value=value
                        )
                    
                    # Set the setting_id
                    cls.objects.create(
                        setting='setting_id',
                        value=settings.APP_SETTING_ID
                    )
                
                # Clear cache after bulk update
                cache.delete('app_settings')
                
        except Exception as e:
            logger.error(f"Error initializing settings: {str(e)}")
            raise

    @classmethod
    def load_settings(cls):
        """Load all settings with cache"""
        cache_key = 'app_settings'
        settings_dict = cache.get(cache_key)
        
        if settings_dict is None:
            settings_dict = {}
            for setting in cls.objects.all():
                try:
                    settings_dict[setting.setting] = setting.value
                except json.JSONDecodeError:
                    settings_dict[setting.setting] = None
            
            # Cache for 1 hour
            cache.set(cache_key, settings_dict, 3600)
        
        return settings_dict

    def save(self, *args, **kwargs):
        """Override save to ensure clean is called"""
        self.full_clean()  # This calls clean()
        super().save(*args, **kwargs)
        # Clear cache after saving
        cache.delete('app_settings')