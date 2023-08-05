# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from . import _utilities
import typing
# Export this package's modules as members:
from .access_token import *
from .alpine_repository import *
from .api_key import *
from .artifact_property_webhook import *
from .artifact_webhook import *
from .artifactory_release_bundle_webhook import *
from .backup import *
from .build_webhook import *
from .certificate import *
from .debian_repository import *
from .distribution_webhook import *
from .docker_v1_repository import *
from .docker_v2_repository import *
from .docker_webhook import *
from .federated_alpine_repository import *
from .federated_bower_repository import *
from .federated_cargo_repository import *
from .federated_chef_repository import *
from .federated_cocoapods_repository import *
from .federated_composer_repository import *
from .federated_conan_repository import *
from .federated_conda_repository import *
from .federated_cran_repository import *
from .federated_debian_repository import *
from .federated_docker_repository import *
from .federated_gems_repository import *
from .federated_generic_repository import *
from .federated_gitltfs_repository import *
from .federated_go_repository import *
from .federated_gradle_repository import *
from .federated_helm_repository import *
from .federated_ivy_repository import *
from .federated_maven_repository import *
from .federated_npm_repository import *
from .federated_nuget_repository import *
from .federated_opkg_repository import *
from .federated_puppet_repository import *
from .federated_pypi_repository import *
from .federated_rpm_repository import *
from .federated_sbt_repository import *
from .federated_vagrant_repository import *
from .general_security import *
from .get_file import *
from .get_fileinfo import *
from .go_repository import *
from .group import *
from .keypair import *
from .ldap_group_setting import *
from .ldap_setting import *
from .local_bower_repository import *
from .local_chef_repository import *
from .local_cocoapods_repository import *
from .local_composer_repository import *
from .local_conan_repository import *
from .local_cran_repository import *
from .local_gems_repository import *
from .local_generic_repository import *
from .local_gitltfs_repository import *
from .local_go_repository import *
from .local_gradle_repository import *
from .local_helm_repository import *
from .local_ivy_repository import *
from .local_maven_repository import *
from .local_npm_repository import *
from .local_nuget_repository import *
from .local_opkg_repository import *
from .local_puppet_repository import *
from .local_pypi_repository import *
from .local_repository import *
from .local_rpm_repository import *
from .local_sbt_repository import *
from .local_vagrant_repository import *
from .maven_repository import *
from .oauth_settings import *
from .permission_target import *
from .permission_targets import *
from .provider import *
from .pull_replication import *
from .push_replication import *
from .release_bundle_webhook import *
from .remote_cargo_repository import *
from .remote_docker_repository import *
from .remote_gradle_repository import *
from .remote_helm_repository import *
from .remote_ivy_repository import *
from .remote_maven_repository import *
from .remote_npm_repository import *
from .remote_pypi_repository import *
from .remote_repository import *
from .remote_sbt_repository import *
from .replication_config import *
from .saml_settings import *
from .single_replication_config import *
from .user import *
from .virtual_conan_repository import *
from .virtual_generic_repository import *
from .virtual_helm_repository import *
from .virtual_repository import *
from .virtual_rpm_repository import *
from .xray_policy import *
from .xray_watch import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_artifactory.config as __config
    config = __config
else:
    config = _utilities.lazy_import('pulumi_artifactory.config')

_utilities.register(
    resource_modules="""
[
 {
  "pkg": "artifactory",
  "mod": "index/accessToken",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/accessToken:AccessToken": "AccessToken"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/alpineRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/alpineRepository:AlpineRepository": "AlpineRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/apiKey",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/apiKey:ApiKey": "ApiKey"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/artifactPropertyWebhook",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/artifactPropertyWebhook:ArtifactPropertyWebhook": "ArtifactPropertyWebhook"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/artifactWebhook",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/artifactWebhook:ArtifactWebhook": "ArtifactWebhook"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/artifactoryReleaseBundleWebhook",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/artifactoryReleaseBundleWebhook:ArtifactoryReleaseBundleWebhook": "ArtifactoryReleaseBundleWebhook"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/backup",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/backup:Backup": "Backup"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/buildWebhook",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/buildWebhook:BuildWebhook": "BuildWebhook"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/certificate",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/certificate:Certificate": "Certificate"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/debianRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/debianRepository:DebianRepository": "DebianRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/distributionWebhook",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/distributionWebhook:DistributionWebhook": "DistributionWebhook"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/dockerV1Repository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/dockerV1Repository:DockerV1Repository": "DockerV1Repository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/dockerV2Repository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/dockerV2Repository:DockerV2Repository": "DockerV2Repository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/dockerWebhook",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/dockerWebhook:DockerWebhook": "DockerWebhook"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedAlpineRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedAlpineRepository:FederatedAlpineRepository": "FederatedAlpineRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedBowerRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedBowerRepository:FederatedBowerRepository": "FederatedBowerRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedCargoRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedCargoRepository:FederatedCargoRepository": "FederatedCargoRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedChefRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedChefRepository:FederatedChefRepository": "FederatedChefRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedCocoapodsRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedCocoapodsRepository:FederatedCocoapodsRepository": "FederatedCocoapodsRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedComposerRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedComposerRepository:FederatedComposerRepository": "FederatedComposerRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedConanRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedConanRepository:FederatedConanRepository": "FederatedConanRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedCondaRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedCondaRepository:FederatedCondaRepository": "FederatedCondaRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedCranRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedCranRepository:FederatedCranRepository": "FederatedCranRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedDebianRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedDebianRepository:FederatedDebianRepository": "FederatedDebianRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedDockerRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedDockerRepository:FederatedDockerRepository": "FederatedDockerRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedGemsRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedGemsRepository:FederatedGemsRepository": "FederatedGemsRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedGenericRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedGenericRepository:FederatedGenericRepository": "FederatedGenericRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedGitltfsRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedGitltfsRepository:FederatedGitltfsRepository": "FederatedGitltfsRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedGoRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedGoRepository:FederatedGoRepository": "FederatedGoRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedGradleRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedGradleRepository:FederatedGradleRepository": "FederatedGradleRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedHelmRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedHelmRepository:FederatedHelmRepository": "FederatedHelmRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedIvyRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedIvyRepository:FederatedIvyRepository": "FederatedIvyRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedMavenRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedMavenRepository:FederatedMavenRepository": "FederatedMavenRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedNpmRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedNpmRepository:FederatedNpmRepository": "FederatedNpmRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedNugetRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedNugetRepository:FederatedNugetRepository": "FederatedNugetRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedOpkgRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedOpkgRepository:FederatedOpkgRepository": "FederatedOpkgRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedPuppetRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedPuppetRepository:FederatedPuppetRepository": "FederatedPuppetRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedPypiRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedPypiRepository:FederatedPypiRepository": "FederatedPypiRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedRpmRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedRpmRepository:FederatedRpmRepository": "FederatedRpmRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedSbtRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedSbtRepository:FederatedSbtRepository": "FederatedSbtRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/federatedVagrantRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/federatedVagrantRepository:FederatedVagrantRepository": "FederatedVagrantRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/generalSecurity",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/generalSecurity:GeneralSecurity": "GeneralSecurity"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/goRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/goRepository:GoRepository": "GoRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/group",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/group:Group": "Group"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/keypair",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/keypair:Keypair": "Keypair"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/ldapGroupSetting",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/ldapGroupSetting:LdapGroupSetting": "LdapGroupSetting"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/ldapSetting",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/ldapSetting:LdapSetting": "LdapSetting"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localBowerRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localBowerRepository:LocalBowerRepository": "LocalBowerRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localChefRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localChefRepository:LocalChefRepository": "LocalChefRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localCocoapodsRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localCocoapodsRepository:LocalCocoapodsRepository": "LocalCocoapodsRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localComposerRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localComposerRepository:LocalComposerRepository": "LocalComposerRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localConanRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localConanRepository:LocalConanRepository": "LocalConanRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localCranRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localCranRepository:LocalCranRepository": "LocalCranRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localGemsRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localGemsRepository:LocalGemsRepository": "LocalGemsRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localGenericRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localGenericRepository:LocalGenericRepository": "LocalGenericRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localGitltfsRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localGitltfsRepository:LocalGitltfsRepository": "LocalGitltfsRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localGoRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localGoRepository:LocalGoRepository": "LocalGoRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localGradleRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localGradleRepository:LocalGradleRepository": "LocalGradleRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localHelmRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localHelmRepository:LocalHelmRepository": "LocalHelmRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localIvyRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localIvyRepository:LocalIvyRepository": "LocalIvyRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localMavenRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localMavenRepository:LocalMavenRepository": "LocalMavenRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localNpmRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localNpmRepository:LocalNpmRepository": "LocalNpmRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localNugetRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localNugetRepository:LocalNugetRepository": "LocalNugetRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localOpkgRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localOpkgRepository:LocalOpkgRepository": "LocalOpkgRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localPuppetRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localPuppetRepository:LocalPuppetRepository": "LocalPuppetRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localPypiRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localPypiRepository:LocalPypiRepository": "LocalPypiRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localRepository:LocalRepository": "LocalRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localRpmRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localRpmRepository:LocalRpmRepository": "LocalRpmRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localSbtRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localSbtRepository:LocalSbtRepository": "LocalSbtRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/localVagrantRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/localVagrantRepository:LocalVagrantRepository": "LocalVagrantRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/mavenRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/mavenRepository:MavenRepository": "MavenRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/oauthSettings",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/oauthSettings:OauthSettings": "OauthSettings"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/permissionTarget",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/permissionTarget:PermissionTarget": "PermissionTarget"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/permissionTargets",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/permissionTargets:PermissionTargets": "PermissionTargets"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/pullReplication",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/pullReplication:PullReplication": "PullReplication"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/pushReplication",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/pushReplication:PushReplication": "PushReplication"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/releaseBundleWebhook",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/releaseBundleWebhook:ReleaseBundleWebhook": "ReleaseBundleWebhook"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/remoteCargoRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/remoteCargoRepository:RemoteCargoRepository": "RemoteCargoRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/remoteDockerRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/remoteDockerRepository:RemoteDockerRepository": "RemoteDockerRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/remoteGradleRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/remoteGradleRepository:RemoteGradleRepository": "RemoteGradleRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/remoteHelmRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/remoteHelmRepository:RemoteHelmRepository": "RemoteHelmRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/remoteIvyRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/remoteIvyRepository:RemoteIvyRepository": "RemoteIvyRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/remoteMavenRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/remoteMavenRepository:RemoteMavenRepository": "RemoteMavenRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/remoteNpmRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/remoteNpmRepository:RemoteNpmRepository": "RemoteNpmRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/remotePypiRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/remotePypiRepository:RemotePypiRepository": "RemotePypiRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/remoteRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/remoteRepository:RemoteRepository": "RemoteRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/remoteSbtRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/remoteSbtRepository:RemoteSbtRepository": "RemoteSbtRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/replicationConfig",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/replicationConfig:ReplicationConfig": "ReplicationConfig"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/samlSettings",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/samlSettings:SamlSettings": "SamlSettings"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/singleReplicationConfig",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/singleReplicationConfig:SingleReplicationConfig": "SingleReplicationConfig"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/user",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/user:User": "User"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/virtualConanRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/virtualConanRepository:VirtualConanRepository": "VirtualConanRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/virtualGenericRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/virtualGenericRepository:VirtualGenericRepository": "VirtualGenericRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/virtualHelmRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/virtualHelmRepository:VirtualHelmRepository": "VirtualHelmRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/virtualRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/virtualRepository:VirtualRepository": "VirtualRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/virtualRpmRepository",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/virtualRpmRepository:VirtualRpmRepository": "VirtualRpmRepository"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/xrayPolicy",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/xrayPolicy:XrayPolicy": "XrayPolicy"
  }
 },
 {
  "pkg": "artifactory",
  "mod": "index/xrayWatch",
  "fqn": "pulumi_artifactory",
  "classes": {
   "artifactory:index/xrayWatch:XrayWatch": "XrayWatch"
  }
 }
]
""",
    resource_packages="""
[
 {
  "pkg": "artifactory",
  "token": "pulumi:providers:artifactory",
  "fqn": "pulumi_artifactory",
  "class": "Provider"
 }
]
"""
)
