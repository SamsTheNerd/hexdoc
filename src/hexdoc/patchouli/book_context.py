from yarl import URL

from hexdoc.core import ResourceDir, ResourceLocation
from hexdoc.data import HexdocMetadata
from hexdoc.model import ValidationContextModel
from hexdoc.patchouli.text import BookLinkBases


class BookContext(ValidationContextModel):
    modid: str
    book_id: ResourceLocation
    link_bases: BookLinkBases
    spoilered_advancements: set[ResourceLocation]
    all_metadata: dict[str, HexdocMetadata]

    def get_link_base(self, resource_dir: ResourceDir) -> URL:
        modid = resource_dir.modid
        if modid is None or modid == self.modid:
            return URL()

        book_url = self.all_metadata[modid].book_url
        if book_url is None:
            raise ValueError(f"Mod {modid} does not export a book url")

        return book_url
