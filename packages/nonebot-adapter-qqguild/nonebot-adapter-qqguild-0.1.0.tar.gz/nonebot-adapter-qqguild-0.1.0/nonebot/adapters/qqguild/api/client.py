from typing import TYPE_CHECKING, List, Optional

from pydantic import Extra, BaseModel

from .model import *

if TYPE_CHECKING:

    class ApiClient:
        async def get_guild(self, guild_id: str) -> Guild:
            ...

        async def me(self) -> User:
            ...

        async def guilds(
            self,
            before: Optional[str] = ...,
            after: Optional[str] = ...,
            limit: Optional[float] = ...,
        ) -> List[Guild]:
            ...

        async def get_channels(self, guild_id: str) -> List[Channel]:
            ...

        async def post_channels(
            self,
            *,
            guild_id: str,
            name: str = ...,
            type: int = ...,
            sub_type: int = ...,
            position: Optional[int] = ...,
            parent_id: Optional[str] = ...,
            private_type: Optional[int] = ...,
            private_user_ids: Optional[List[str]] = ...,
        ) -> List[Channel]:
            ...

        async def get_channel(self, channel_id: str) -> Channel:
            ...

        async def patch_channel(
            self,
            *,
            channel_id: str,
            name: Optional[str] = ...,
            type: Optional[int] = ...,
            sub_type: Optional[int] = ...,
            position: Optional[int] = ...,
            parent_id: Optional[str] = ...,
            private_type: Optional[int] = ...,
        ) -> Channel:
            ...

        async def delete_channel(self, channel_id: str) -> None:
            ...

        async def get_members(
            self,
            guild_id: str,
            after: Optional[str] = ...,
            limit: Optional[float] = ...,
        ) -> List[Member]:
            ...

        async def get_member(self, guild_id: str, user_id: str) -> Member:
            ...

        async def delete_member(
            self, *, guild_id: str, user_id: str, add_blacklist: Optional[bool] = ...
        ) -> None:
            ...

        async def get_guild_roles(self, guild_id: str) -> GetGuildRolesReturn:
            ...

        async def post_guild_role(
            self,
            *,
            guild_id: str,
            name: str = ...,
            color: Optional[float] = ...,
            hoist: Optional[float] = ...,
        ) -> PostGuildRoleReturn:
            ...

        async def patch_guild_role(
            self,
            *,
            guild_id: str,
            role_id: str,
            name: Optional[str] = ...,
            color: Optional[float] = ...,
            hoist: Optional[float] = ...,
        ) -> PatchGuildRoleReturn:
            ...

        async def delete_guild_role(self, guild_id: str, role_id: str) -> None:
            ...

        async def put_guild_member_role(
            self, *, guild_id: str, role_id: str, user_id: str, id: Optional[str] = ...
        ) -> None:
            ...

        async def delete_guild_member_role(
            self, *, guild_id: str, role_id: str, user_id: str, id: Optional[str] = ...
        ) -> None:
            ...

        async def get_channel_permissions(
            self, channel_id: str, user_id: str
        ) -> ChannelPermissions:
            ...

        async def put_channel_permissions(
            self,
            *,
            channel_id: str,
            user_id: str,
            add: Optional[str] = ...,
            remove: Optional[str] = ...,
        ) -> None:
            ...

        async def get_channel_roles_permissions(
            self, channel_id: str, role_id: str
        ) -> ChannelPermissions:
            ...

        async def put_channel_roles_permissions(
            self,
            *,
            channel_id: str,
            role_id: str,
            add: Optional[str] = ...,
            remove: Optional[str] = ...,
        ) -> None:
            ...

        async def get_message_of_id(self, channel_id: str, message_id: str) -> Message:
            ...

        async def post_messages(
            self,
            *,
            channel_id: str,
            content: Optional[str] = ...,
            embed: Optional[MessageEmbed] = ...,
            ark: Optional[MessageArk] = ...,
            message_reference: Optional[MessageReference] = ...,
            image: Optional[str] = ...,
            msg_id: Optional[str] = ...,
        ) -> Message:
            ...

        async def post_dms(
            self, *, recipient_id: str = ..., source_guild_id: str = ...
        ) -> List[DMS]:
            ...

        async def post_dms_messages(
            self,
            *,
            guild_id: str,
            content: Optional[str] = ...,
            embed: Optional[MessageEmbed] = ...,
            ark: Optional[MessageArk] = ...,
            message_reference: Optional[MessageReference] = ...,
            image: Optional[str] = ...,
            msg_id: Optional[str] = ...,
        ) -> List[Message]:
            ...

        async def patch_guild_mute(
            self,
            *,
            guild_id: str,
            mute_end_timestamp: Optional[str] = ...,
            mute_seconds: Optional[str] = ...,
        ) -> None:
            ...

        async def patch_guild_member_mute(
            self,
            *,
            guild_id: str,
            user_id: str,
            mute_end_timestamp: Optional[str] = ...,
            mute_seconds: Optional[str] = ...,
        ) -> None:
            ...

        async def post_guild_announces(
            self, *, guild_id: str, message_id: str = ..., channel_id: str = ...
        ) -> None:
            ...

        async def delete_guild_announces(self, guild_id: str, message_id: str) -> None:
            ...

        async def post_channel_announces(
            self, *, channel_id: str, message_id: str = ...
        ) -> Announces:
            ...

        async def delete_channel_announces(
            self, channel_id: str, message_id: str
        ) -> None:
            ...

        async def get_schedules(
            self, *, channel_id: str, since: Optional[int] = ...
        ) -> List[Schedule]:
            ...

        async def post_schedule(
            self,
            *,
            channel_id: str,
            name: str = ...,
            description: Optional[str] = ...,
            start_timestamp: str = ...,
            end_timestamp: str = ...,
            creator: Optional[Member] = ...,
            jump_channel_id: Optional[str] = ...,
            remind_type: str = ...,
        ) -> Schedule:
            ...

        async def get_schedule(self, channel_id: str, schedule_id: str) -> Schedule:
            ...

        async def patch_schedule(
            self,
            *,
            channel_id: str,
            schedule_id: str,
            name: Optional[str] = ...,
            description: Optional[str] = ...,
            start_timestamp: Optional[str] = ...,
            end_timestamp: Optional[str] = ...,
            creator: Optional[Member] = ...,
            jump_channel_id: Optional[str] = ...,
            remind_type: Optional[str] = ...,
        ) -> Schedule:
            ...

        async def delete_schedule(self, channel_id: str, schedule_id: str) -> None:
            ...

        async def audio_control(
            self,
            *,
            channel_id: str,
            audio_url: Optional[str] = ...,
            text: Optional[str] = ...,
            status: Optional[int] = ...,
        ) -> None:
            ...

        async def get_guild_api_permission(self, guild_id: str) -> List[APIPermission]:
            ...

        async def post_api_permission_demand(
            self,
            *,
            guild_id: str,
            channel_id: Optional[str] = ...,
            api_identify: Optional[APIPermissionDemandIdentify] = ...,
            desc: Optional[str] = ...,
        ) -> List[APIPermissionDemand]:
            ...

        async def url_get(self) -> UrlGetReturn:
            ...

        async def shard_url_get(self) -> ShardUrlGetReturn:
            ...

        async def put_message_reaction(
            self, channel_id: str, message_id: str, type: int, id: str
        ) -> None:
            ...

        async def delete_own_message_reaction(
            self, channel_id: str, message_id: str, type: int, id: str
        ) -> None:
            ...

        async def put_pins_message(self, channel_id: str, message_id: str) -> None:
            ...

        async def delete_pins_message(self, channel_id: str, message_id: str) -> None:
            ...

        async def get_pins_message(self, channel_id: str) -> PinsMessage:
            ...

else:

    class ApiClient:
        ...
