"""
Type annotations for elbv2 service client paginators.

[Open documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elbv2.client import ElasticLoadBalancingv2Client
    from types_aiobotocore_elbv2.paginator import (
        DescribeAccountLimitsPaginator,
        DescribeListenerCertificatesPaginator,
        DescribeListenersPaginator,
        DescribeLoadBalancersPaginator,
        DescribeRulesPaginator,
        DescribeSSLPoliciesPaginator,
        DescribeTargetGroupsPaginator,
    )

    session = get_session()
    with session.create_client("elbv2") as client:
        client: ElasticLoadBalancingv2Client

        describe_account_limits_paginator: DescribeAccountLimitsPaginator = client.get_paginator("describe_account_limits")
        describe_listener_certificates_paginator: DescribeListenerCertificatesPaginator = client.get_paginator("describe_listener_certificates")
        describe_listeners_paginator: DescribeListenersPaginator = client.get_paginator("describe_listeners")
        describe_load_balancers_paginator: DescribeLoadBalancersPaginator = client.get_paginator("describe_load_balancers")
        describe_rules_paginator: DescribeRulesPaginator = client.get_paginator("describe_rules")
        describe_ssl_policies_paginator: DescribeSSLPoliciesPaginator = client.get_paginator("describe_ssl_policies")
        describe_target_groups_paginator: DescribeTargetGroupsPaginator = client.get_paginator("describe_target_groups")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import LoadBalancerTypeEnumType
from .type_defs import (
    DescribeAccountLimitsOutputTypeDef,
    DescribeListenerCertificatesOutputTypeDef,
    DescribeListenersOutputTypeDef,
    DescribeLoadBalancersOutputTypeDef,
    DescribeRulesOutputTypeDef,
    DescribeSSLPoliciesOutputTypeDef,
    DescribeTargetGroupsOutputTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "DescribeAccountLimitsPaginator",
    "DescribeListenerCertificatesPaginator",
    "DescribeListenersPaginator",
    "DescribeLoadBalancersPaginator",
    "DescribeRulesPaginator",
    "DescribeSSLPoliciesPaginator",
    "DescribeTargetGroupsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAccountLimitsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeAccountLimits)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describeaccountlimitspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[DescribeAccountLimitsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeAccountLimits.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describeaccountlimitspaginator)
        """


class DescribeListenerCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeListenerCertificates)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describelistenercertificatespaginator)
    """

    def paginate(
        self, *, ListenerArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[DescribeListenerCertificatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeListenerCertificates.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describelistenercertificatespaginator)
        """


class DescribeListenersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeListeners)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describelistenerspaginator)
    """

    def paginate(
        self,
        *,
        LoadBalancerArn: str = ...,
        ListenerArns: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[DescribeListenersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeListeners.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describelistenerspaginator)
        """


class DescribeLoadBalancersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeLoadBalancers)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describeloadbalancerspaginator)
    """

    def paginate(
        self,
        *,
        LoadBalancerArns: Sequence[str] = ...,
        Names: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[DescribeLoadBalancersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeLoadBalancers.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describeloadbalancerspaginator)
        """


class DescribeRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeRules)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describerulespaginator)
    """

    def paginate(
        self,
        *,
        ListenerArn: str = ...,
        RuleArns: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[DescribeRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeRules.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describerulespaginator)
        """


class DescribeSSLPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeSSLPolicies)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describesslpoliciespaginator)
    """

    def paginate(
        self,
        *,
        Names: Sequence[str] = ...,
        LoadBalancerType: LoadBalancerTypeEnumType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[DescribeSSLPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeSSLPolicies.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describesslpoliciespaginator)
        """


class DescribeTargetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeTargetGroups)
    [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describetargetgroupspaginator)
    """

    def paginate(
        self,
        *,
        LoadBalancerArn: str = ...,
        TargetGroupArns: Sequence[str] = ...,
        Names: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[DescribeTargetGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Paginator.DescribeTargetGroups.paginate)
        [Show types-aiobotocore documentation](https://vemel.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators.html#describetargetgroupspaginator)
        """
