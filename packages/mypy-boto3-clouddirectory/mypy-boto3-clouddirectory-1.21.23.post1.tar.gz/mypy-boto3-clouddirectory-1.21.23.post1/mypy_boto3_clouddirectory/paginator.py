"""
Type annotations for clouddirectory service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_clouddirectory.client import CloudDirectoryClient
    from mypy_boto3_clouddirectory.paginator import (
        ListAppliedSchemaArnsPaginator,
        ListAttachedIndicesPaginator,
        ListDevelopmentSchemaArnsPaginator,
        ListDirectoriesPaginator,
        ListFacetAttributesPaginator,
        ListFacetNamesPaginator,
        ListIncomingTypedLinksPaginator,
        ListIndexPaginator,
        ListManagedSchemaArnsPaginator,
        ListObjectAttributesPaginator,
        ListObjectParentPathsPaginator,
        ListObjectPoliciesPaginator,
        ListOutgoingTypedLinksPaginator,
        ListPolicyAttachmentsPaginator,
        ListPublishedSchemaArnsPaginator,
        ListTagsForResourcePaginator,
        ListTypedLinkFacetAttributesPaginator,
        ListTypedLinkFacetNamesPaginator,
        LookupPolicyPaginator,
    )

    session = Session()
    client: CloudDirectoryClient = session.client("clouddirectory")

    list_applied_schema_arns_paginator: ListAppliedSchemaArnsPaginator = client.get_paginator("list_applied_schema_arns")
    list_attached_indices_paginator: ListAttachedIndicesPaginator = client.get_paginator("list_attached_indices")
    list_development_schema_arns_paginator: ListDevelopmentSchemaArnsPaginator = client.get_paginator("list_development_schema_arns")
    list_directories_paginator: ListDirectoriesPaginator = client.get_paginator("list_directories")
    list_facet_attributes_paginator: ListFacetAttributesPaginator = client.get_paginator("list_facet_attributes")
    list_facet_names_paginator: ListFacetNamesPaginator = client.get_paginator("list_facet_names")
    list_incoming_typed_links_paginator: ListIncomingTypedLinksPaginator = client.get_paginator("list_incoming_typed_links")
    list_index_paginator: ListIndexPaginator = client.get_paginator("list_index")
    list_managed_schema_arns_paginator: ListManagedSchemaArnsPaginator = client.get_paginator("list_managed_schema_arns")
    list_object_attributes_paginator: ListObjectAttributesPaginator = client.get_paginator("list_object_attributes")
    list_object_parent_paths_paginator: ListObjectParentPathsPaginator = client.get_paginator("list_object_parent_paths")
    list_object_policies_paginator: ListObjectPoliciesPaginator = client.get_paginator("list_object_policies")
    list_outgoing_typed_links_paginator: ListOutgoingTypedLinksPaginator = client.get_paginator("list_outgoing_typed_links")
    list_policy_attachments_paginator: ListPolicyAttachmentsPaginator = client.get_paginator("list_policy_attachments")
    list_published_schema_arns_paginator: ListPublishedSchemaArnsPaginator = client.get_paginator("list_published_schema_arns")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_typed_link_facet_attributes_paginator: ListTypedLinkFacetAttributesPaginator = client.get_paginator("list_typed_link_facet_attributes")
    list_typed_link_facet_names_paginator: ListTypedLinkFacetNamesPaginator = client.get_paginator("list_typed_link_facet_names")
    lookup_policy_paginator: LookupPolicyPaginator = client.get_paginator("lookup_policy")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import ConsistencyLevelType, DirectoryStateType
from .type_defs import (
    ListAppliedSchemaArnsResponseTypeDef,
    ListAttachedIndicesResponseTypeDef,
    ListDevelopmentSchemaArnsResponseTypeDef,
    ListDirectoriesResponseTypeDef,
    ListFacetAttributesResponseTypeDef,
    ListFacetNamesResponseTypeDef,
    ListIncomingTypedLinksResponseTypeDef,
    ListIndexResponseTypeDef,
    ListManagedSchemaArnsResponseTypeDef,
    ListObjectAttributesResponseTypeDef,
    ListObjectParentPathsResponseTypeDef,
    ListObjectPoliciesResponseTypeDef,
    ListOutgoingTypedLinksResponseTypeDef,
    ListPolicyAttachmentsResponseTypeDef,
    ListPublishedSchemaArnsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTypedLinkFacetAttributesResponseTypeDef,
    ListTypedLinkFacetNamesResponseTypeDef,
    LookupPolicyResponseTypeDef,
    ObjectAttributeRangeTypeDef,
    ObjectReferenceTypeDef,
    PaginatorConfigTypeDef,
    SchemaFacetTypeDef,
    TypedLinkAttributeRangeTypeDef,
    TypedLinkSchemaAndFacetNameTypeDef,
)

__all__ = (
    "ListAppliedSchemaArnsPaginator",
    "ListAttachedIndicesPaginator",
    "ListDevelopmentSchemaArnsPaginator",
    "ListDirectoriesPaginator",
    "ListFacetAttributesPaginator",
    "ListFacetNamesPaginator",
    "ListIncomingTypedLinksPaginator",
    "ListIndexPaginator",
    "ListManagedSchemaArnsPaginator",
    "ListObjectAttributesPaginator",
    "ListObjectParentPathsPaginator",
    "ListObjectPoliciesPaginator",
    "ListOutgoingTypedLinksPaginator",
    "ListPolicyAttachmentsPaginator",
    "ListPublishedSchemaArnsPaginator",
    "ListTagsForResourcePaginator",
    "ListTypedLinkFacetAttributesPaginator",
    "ListTypedLinkFacetNamesPaginator",
    "LookupPolicyPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAppliedSchemaArnsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListAppliedSchemaArns)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listappliedschemaarnspaginator)
    """

    def paginate(
        self,
        *,
        DirectoryArn: str,
        SchemaArn: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAppliedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListAppliedSchemaArns.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listappliedschemaarnspaginator)
        """


class ListAttachedIndicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListAttachedIndices)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listattachedindicespaginator)
    """

    def paginate(
        self,
        *,
        DirectoryArn: str,
        TargetReference: "ObjectReferenceTypeDef",
        ConsistencyLevel: ConsistencyLevelType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAttachedIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListAttachedIndices.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listattachedindicespaginator)
        """


class ListDevelopmentSchemaArnsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListDevelopmentSchemaArns)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listdevelopmentschemaarnspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDevelopmentSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListDevelopmentSchemaArns.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listdevelopmentschemaarnspaginator)
        """


class ListDirectoriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListDirectories)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listdirectoriespaginator)
    """

    def paginate(
        self, *, state: DirectoryStateType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDirectoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListDirectories.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listdirectoriespaginator)
        """


class ListFacetAttributesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListFacetAttributes)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listfacetattributespaginator)
    """

    def paginate(
        self, *, SchemaArn: str, Name: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFacetAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListFacetAttributes.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listfacetattributespaginator)
        """


class ListFacetNamesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListFacetNames)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listfacetnamespaginator)
    """

    def paginate(
        self, *, SchemaArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFacetNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListFacetNames.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listfacetnamespaginator)
        """


class ListIncomingTypedLinksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListIncomingTypedLinks)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listincomingtypedlinkspaginator)
    """

    def paginate(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: "ObjectReferenceTypeDef",
        FilterAttributeRanges: Sequence["TypedLinkAttributeRangeTypeDef"] = ...,
        FilterTypedLink: "TypedLinkSchemaAndFacetNameTypeDef" = ...,
        ConsistencyLevel: ConsistencyLevelType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListIncomingTypedLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListIncomingTypedLinks.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listincomingtypedlinkspaginator)
        """


class ListIndexPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListIndex)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listindexpaginator)
    """

    def paginate(
        self,
        *,
        DirectoryArn: str,
        IndexReference: "ObjectReferenceTypeDef",
        RangesOnIndexedValues: Sequence["ObjectAttributeRangeTypeDef"] = ...,
        ConsistencyLevel: ConsistencyLevelType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListIndexResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListIndex.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listindexpaginator)
        """


class ListManagedSchemaArnsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListManagedSchemaArns)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listmanagedschemaarnspaginator)
    """

    def paginate(
        self, *, SchemaArn: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListManagedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListManagedSchemaArns.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listmanagedschemaarnspaginator)
        """


class ListObjectAttributesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListObjectAttributes)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listobjectattributespaginator)
    """

    def paginate(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: "ObjectReferenceTypeDef",
        ConsistencyLevel: ConsistencyLevelType = ...,
        FacetFilter: "SchemaFacetTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListObjectAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListObjectAttributes.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listobjectattributespaginator)
        """


class ListObjectParentPathsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListObjectParentPaths)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listobjectparentpathspaginator)
    """

    def paginate(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: "ObjectReferenceTypeDef",
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListObjectParentPathsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListObjectParentPaths.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listobjectparentpathspaginator)
        """


class ListObjectPoliciesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListObjectPolicies)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listobjectpoliciespaginator)
    """

    def paginate(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: "ObjectReferenceTypeDef",
        ConsistencyLevel: ConsistencyLevelType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListObjectPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListObjectPolicies.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listobjectpoliciespaginator)
        """


class ListOutgoingTypedLinksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListOutgoingTypedLinks)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listoutgoingtypedlinkspaginator)
    """

    def paginate(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: "ObjectReferenceTypeDef",
        FilterAttributeRanges: Sequence["TypedLinkAttributeRangeTypeDef"] = ...,
        FilterTypedLink: "TypedLinkSchemaAndFacetNameTypeDef" = ...,
        ConsistencyLevel: ConsistencyLevelType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOutgoingTypedLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListOutgoingTypedLinks.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listoutgoingtypedlinkspaginator)
        """


class ListPolicyAttachmentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListPolicyAttachments)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listpolicyattachmentspaginator)
    """

    def paginate(
        self,
        *,
        DirectoryArn: str,
        PolicyReference: "ObjectReferenceTypeDef",
        ConsistencyLevel: ConsistencyLevelType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPolicyAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListPolicyAttachments.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listpolicyattachmentspaginator)
        """


class ListPublishedSchemaArnsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListPublishedSchemaArns)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listpublishedschemaarnspaginator)
    """

    def paginate(
        self, *, SchemaArn: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPublishedSchemaArnsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListPublishedSchemaArns.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listpublishedschemaarnspaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListTagsForResource)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listtagsforresourcepaginator)
    """

    def paginate(
        self, *, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listtagsforresourcepaginator)
        """


class ListTypedLinkFacetAttributesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListTypedLinkFacetAttributes)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listtypedlinkfacetattributespaginator)
    """

    def paginate(
        self, *, SchemaArn: str, Name: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTypedLinkFacetAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListTypedLinkFacetAttributes.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listtypedlinkfacetattributespaginator)
        """


class ListTypedLinkFacetNamesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListTypedLinkFacetNames)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listtypedlinkfacetnamespaginator)
    """

    def paginate(
        self, *, SchemaArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTypedLinkFacetNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.ListTypedLinkFacetNames.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#listtypedlinkfacetnamespaginator)
        """


class LookupPolicyPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.LookupPolicy)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#lookuppolicypaginator)
    """

    def paginate(
        self,
        *,
        DirectoryArn: str,
        ObjectReference: "ObjectReferenceTypeDef",
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[LookupPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/clouddirectory.html#CloudDirectory.Paginator.LookupPolicy.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/paginators.html#lookuppolicypaginator)
        """
