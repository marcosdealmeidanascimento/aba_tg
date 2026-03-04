from core.models.auditoria import AuditLog


def log_action(user, acao, descricao, request):
    ip = request.META.get('REMOTE_ADDR')
    ua = request.META.get('HTTP_USER_AGENT', 'unknown')
    AuditLog.objects.create(
        usuario=user if user.is_authenticated else None,
        acao=acao, descricao=descricao, ip_address=ip, user_agent=ua
    )
