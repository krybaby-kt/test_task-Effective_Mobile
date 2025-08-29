"""
Эндпоинты панели администратора.

Маршруты для административных операций. Все эндпоинты требуют право "admin_panel".
"""
from fastapi import APIRouter, Request, Depends, HTTPException, status
from web_api.dependencies.rules_auth import require_rule
from fastapi.responses import JSONResponse
from web_api.endpoints.admin_panel.schematics import AdminPanelResponse, RolesAndRulesResponse, CreateRoleRequest, CreateRoleResponse, CreateRuleRequest, CreateRuleResponse, CreateRoleRuleRequest, CreateRoleRuleResponse, DeleteRoleRequest, DeleteRoleResponse, DeleteRuleRequest, DeleteRuleResponse, DeleteRoleRuleRequest, DeleteRoleRuleResponse, RulesResponse, RolesResponse, RuleItem, RoleItem

from database.tools.role_rules import RoleRuleTool
from database.tools.roles import RoleTool
from database.tools.rules import RuleTool

from database.models.roles import RoleModel
from database.models.rules import RuleModel
from database.models.role_rules import RoleRuleModel

# Router для административной панели с обязательной проверкой прав админа
router = APIRouter(dependencies=[require_rule("admin_panel")])


@router.get(
    '/', 
    description="Панель администратора",
    response_model=AdminPanelResponse,
    response_model_exclude_none=True
)
async def web_api_admin_panel(
    request: Request,
):
    """
    Основной эндпоинт административной панели.
    
    Доступен только пользователям с правом "admin_panel".
    Предоставляет доступ к административному функционалу.
    
    Args:
        request: HTTP запрос
        
    Returns:
        JSON ответ с подтверждением успешного доступа к панели
        
    Note:
        Автоматически проверяет права пользователя через require_rule dependency
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )


@router.get(
    '/rules',
    description="Получить список правил",
    response_model=RulesResponse,
    response_model_exclude_none=True
)
async def web_api_get_rules(
    request: Request,
):
    """
    Получает полный список всех правил доступа в системе.
    
    Возвращает все правила с их именами и комментариями для управления.
    Используется для отображения доступных правил в административной панели.
    Доступен только администраторам.
    
    Args:
        request: HTTP запрос
        
    Returns:
        JSON ответ со списком правил в формате [{name: str, comment: str}]
    """
    dbRules = await RuleTool.get_all()
    content = [
        dict(name=rule.name, comment=rule.comment)
        for rule in dbRules
    ]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True,
            content=content
        )
    )


@router.get(
    '/roles',
    description="Получить список ролей",
    response_model=RolesResponse,
    response_model_exclude_none=True
)
async def web_api_get_roles(
    request: Request,
):
    """
    Получает полный список всех ролей в системе.
    
    Возвращает все роли с их именами и комментариями для управления.
    Используется для отображения доступных ролей в административной панели.
    Доступен только администраторам.
    
    Args:
        request: HTTP запрос
        
    Returns:
        JSON ответ со списком ролей в формате [{name: str, comment: str}]
    """
    dbRoles = await RoleTool.get_all()
    content = [
        dict(name=role.name, comment=role.comment)
        for role in dbRoles
    ]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True,
            content=content
        )
    )


@router.get(
    '/roles-and-rules',
    description="Получить список ролей и прав",
    response_model=RolesAndRulesResponse,
    response_model_exclude_none=True
)
async def web_api_get_users(
    request: Request,
):
    """
    Получает структурированный список всех ролей с их правами.
    
    Формирует словарь, где ключ - роль, значение - список связанных правил.
    Доступен только администраторам.
    
    Args:
        request: HTTP запрос
        
    Returns:
        JSON ответ со списком ролей и их правами в формате [{role: str, rules: [str]}]
    """
    dbRoleRules = await RoleRuleTool.get_all()
    
    roles_rules_dict = {}
    for role_rule in dbRoleRules:
        role_name = role_rule.role_name
        rule_name = role_rule.rule_name
        
        if role_name not in roles_rules_dict:
            roles_rules_dict[role_name] = []
        
        if rule_name not in roles_rules_dict[role_name]:
            roles_rules_dict[role_name].append(rule_name)
    
    content = [
        dict(role=role, rules=rules) 
        for role, rules in roles_rules_dict.items()
    ]
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True,
            content=content
        )
    )


@router.post(
    '/create-role',
    description="Создать роль",
    response_model=CreateRoleResponse,
    response_model_exclude_none=True
)
async def web_api_create_role(
    request: Request,
    role_data: CreateRoleRequest
):
    """
    Создает новую роль в системе.
    
    Добавляет роль с указанным именем и комментарием в базу данных.
    Проверяет уникальность имени роли перед созданием.
    
    Args:
        request: HTTP запрос
        role_data: Данные для создания роли (имя и комментарий)
        
    Returns:
        JSON ответ с результатом операции
    """

    if await RoleTool(role_data.name).get():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exists")

    await RoleTool.create(data=dict(
        name=role_data.name,
        comment=role_data.comment
    ))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )


@router.post(
    '/create-rule',
    description="Создать правило",
    response_model=CreateRuleResponse,
    response_model_exclude_none=True
)
async def web_api_create_rule(
    request: Request,
    rule_data: CreateRuleRequest
):
    """
    Создает новое правило доступа в системе.
    
    Добавляет правило с указанным именем и комментарием в базу данных.
    Проверяет уникальность имени правила перед созданием.
    
    Args:
        request: HTTP запрос
        rule_data: Данные для создания правила (имя и комментарий)
        
    Returns:
        JSON ответ с результатом операции
    """
    if await RuleTool(rule_data.name).get():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rule already exists")

    await RuleTool.create(data=dict(
        name=rule_data.name,
        comment=rule_data.comment
    ))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )   


@router.post(
    '/create-role-rule',
    description="Создать связь между ролью и правилом",
    response_model=CreateRoleRuleResponse,
    response_model_exclude_none=True
)
async def web_api_create_role_rule(
    request: Request,
    role_rule_data: CreateRoleRuleRequest
):
    """
    Создает связь между ролью и правилом (назначает право роли).
    
    Устанавливает отношение Many-to-Many между указанной ролью и правилом.
    Проверяет существование роли и правила, а также уникальность связи.
    
    Args:
        request: HTTP запрос
        role_rule_data: Данные связи (имя роли и имя правила)
        
    Returns:
        JSON ответ с результатом операции
        
    Raises:
        HTTPException: Если связь уже существует, роль не найдена или правило не найдено
    """
    if await RoleRuleTool.get_by_role_name_and_rule_name(role_name=role_rule_data.role_name, rule_name=role_rule_data.rule_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role rule already exists")
    if not await RoleTool(role_rule_data.role_name).get():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role not found")
    if not await RuleTool(role_rule_data.rule_name).get():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rule not found")

    await RoleRuleTool.create(data=dict(
        role_name=role_rule_data.role_name,
        rule_name=role_rule_data.rule_name
    ))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )

@router.post(
    '/delete-role',
    description="Удалить роль",
    response_model=DeleteRoleResponse,
    response_model_exclude_none=True
)
async def web_api_delete_role(
    request: Request,
    role_data: DeleteRoleRequest
):
    """
    Удаляет роль из системы.
    
    Полностью удаляет роль и все связанные с ней права (role_rules).
    Проверяет, что роль не назначена ни одному пользователю перед удалением.
    
    Args:
        request: HTTP запрос
        role_data: Данные для удаления (имя роли)
        
    Returns:
        JSON ответ с результатом операции
        
    Raises:
        HTTPException: Если роль не найдена или назначена хотя бы одному пользователю
    """
    if not await RoleTool(role_data.name).get():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role not found")
    
    # Проверяем, есть ли пользователи с этой ролью
    from database.tools.users import UserTool
    from database.models.users import UserModel
    users_with_role = await UserTool.get_all_with_filters(filters=[UserModel.role == role_data.name])
    if users_with_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Cannot delete role: {len(users_with_role)} user(s) still have this role"
        )

    await RoleTool(role_data.name).delete()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )

@router.post(
    '/delete-rule',
    description="Удалить правило",
    response_model=DeleteRuleResponse,
    response_model_exclude_none=True
)
async def web_api_delete_rule(
    request: Request,
    rule_data: DeleteRuleRequest
):
    """
    Удаляет правило доступа из системы.
    
    Полностью удаляет правило и все связи с ролями.
    Пользователи больше не смогут использовать это правило.
    
    Args:
        request: HTTP запрос
        rule_data: Данные для удаления (имя правила)
        
    Returns:
        JSON ответ с результатом операции
        
    Raises:
        HTTPException: Если правило с указанным именем не найдено
        
    Warning:
        Операция необратима. Проверьте, что правило не используется в системе безопасности.
    """
    if not await RuleTool(rule_data.name).get():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rule not found")

    await RuleTool(rule_data.name).delete()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )

@router.post(
    '/delete-role-rule',
    description="Удалить связь между ролью и правилом",
    response_model=DeleteRoleRuleResponse,
    response_model_exclude_none=True
)
async def web_api_delete_role_rule(
    request: Request,
    role_rule_data: DeleteRoleRuleRequest
):
    """
    Удаляет связь между ролью и правилом (отзывает право у роли).
    
    Убирает конкретное правило у указанной роли, не затрагивая саму роль или правило.
    Пользователи с этой ролью потеряют доступ к данному функционалу.
    
    Args:
        request: HTTP запрос
        role_rule_data: Данные для удаления связи (имя роли и имя правила)
        
    Returns:
        JSON ответ с результатом операции
        
    Note:
        Если связь не найдена, операция завершится успешно без ошибки.
    """
    dbRoleRule = await RoleRuleTool.get_by_role_name_and_rule_name(role_name=role_rule_data.role_name, rule_name=role_rule_data.rule_name)
    if not dbRoleRule:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role rule not found")


    await RoleRuleTool(dbRoleRule.id).delete()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(
            success=True
        )
    )   