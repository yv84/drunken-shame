from storages.backends.s3boto import S3BotoStorage

StaticRootS3BotoStorage = lambda: S3BotoStorage(location='site_static')
MediaRootS3BotoStorage  = lambda: S3BotoStorage(location='site_media')
