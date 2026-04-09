#!/usr/bin/env python3
"""Replace Figma MCP asset URLs in index.html with SVG sprite + picsum photos."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
FIGMA_BASE = "https://www.figma.com/api/mcp/asset/"

SPRITE = """<!-- Static icons: Figma MCP URLs require MCP session; replaced for static hosting -->
    <svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false" style="position:absolute;width:0;height:0;overflow:hidden">
      <symbol id="icon-cb-solid-on" viewBox="0 0 24 24">
        <rect x="0" y="0" width="24" height="24" rx="8" fill="#00a759" />
        <g transform="translate(12 12) scale(0.68) translate(-12 -12)">
          <path fill="#fff" d="M9 16.17 4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
        </g>
      </symbol>
      <symbol id="icon-cb-header-on" viewBox="0 0 24 24">
        <rect x="0" y="0" width="24" height="24" rx="8" fill="none" stroke="#fff" stroke-width="1.5" />
        <g transform="translate(12 12) scale(0.68) translate(-12 -12)">
          <path fill="#fff" d="M9 16.17 4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
        </g>
      </symbol>
      <symbol id="icon-chev-down-white" viewBox="0 0 12 8">
        <path d="M1 1.5 6 6.5 11 1.5" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
      </symbol>
      <symbol id="icon-chev-right" viewBox="0 0 24 24">
        <path d="M9 6l6 6-6 6 1.4 1.4 7.4-7.4-7.4-7.4z" fill="#8b8b8b" />
      </symbol>
      <symbol id="icon-chev-up" viewBox="0 0 24 24">
        <path d="M7.4 15.4 12 10.8l4.6 4.6 1.4-1.4-6-6-6 6z" fill="#8b8b8b" />
      </symbol>
      <symbol id="icon-store" viewBox="0 0 24 24">
        <path fill="#00a759" d="M4 8V6a2 2 0 012-2h12a2 2 0 012 2v2H4zm0 2h16v10a2 2 0 01-2 2H6a2 2 0 01-2-2V10zm4 4v4h8v-4H8z" />
      </symbol>
      <symbol id="icon-truck" viewBox="0 0 24 24">
        <path fill="#00a759" d="M3 6h11v10h-2v2H3V6zm13 0h3l3 4v6h-2v2h-4v-4h2v-2h2v-2.5L18.2 8H16V6zm-9 12a2 2 0 100-4 2 2 0 000 4zm8 0h2v-2h-2v2z" />
      </symbol>
      <symbol id="icon-info" viewBox="0 0 24 24">
        <path fill="#8b8b8b" d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z" />
      </symbol>
      <symbol id="icon-chev-small" viewBox="0 0 16 16">
        <path d="M6 4l4 4-4 4" fill="none" stroke="#00a759" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
      </symbol>
      <symbol id="icon-alert" viewBox="0 0 24 24">
        <path fill="#0172ce" d="M12 2 2 20h20L12 2zm1 13h-2v-2h2v2zm0-4h-2V8h2v3z" />
      </symbol>
      <symbol id="icon-heart" viewBox="0 0 24 24">
        <path fill="none" stroke="#8b8b8b" stroke-width="1.5" d="M12 21s-7-4.35-7-10a4.5 4.5 0 017.09-3.7A4.5 4.5 0 0119 11c0 5.65-7 10-7 10z" />
      </symbol>
      <symbol id="icon-trash" viewBox="0 0 24 24">
        <path fill="#575757" d="M6 7h12v2H6V7zm2 3h10v10a2 2 0 01-2 2H10a2 2 0 01-2-2V10zm3 2v6h2v-6h-2zm4 0v6h2v-6h-2zM9 4h6l1 1h4v2H4V5h4l1-1z" />
      </symbol>
      <symbol id="icon-cart-white" viewBox="0 0 24 24">
        <path fill="#ffffff" d="M7 18a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm10 0a1.5 1.5 0 100 3 1.5 1.5 0 000-3zM7.2 14h9.45a2 2 0 001.75-1l3.25-6H6.2l-1-2H2V4h3.2l1 2h16l-4 8a4 4 0 01-3.55 2H8.8l-1.1 2z" />
      </symbol>
      <symbol id="icon-promo-tag" viewBox="0 0 24 24">
        <path fill="#ff6c40" d="M4 4h8l8 8-8 8-8-8V4zm4 4h4v4H8V8z" opacity="0.9" />
      </symbol>
      <symbol id="icon-promo-corner" viewBox="0 0 24 24">
        <path fill="#cf062a" d="M0 24V0h14L0 24z" />
      </symbol>
      <symbol id="icon-close" viewBox="0 0 24 24">
        <path fill="#575757" d="M18.3 5.7 12 12l6.3 6.3-1.4 1.4L10.6 13.4 4.3 19.7 2.9 18.3 9.2 12 2.9 5.7 4.3 4.3 10.6 10.6l6.3-6.3z" />
      </symbol>
      <symbol id="icon-grabber" viewBox="0 0 48 6">
        <rect x="8" y="2" width="32" height="2" rx="1" fill="#d7dbe0" />
      </symbol>
    </svg>
"""


def replace_all_img(html: str, uuid: str, replacement: str) -> str:
    """Match one <img> tag only — do not let .* span past the first closing >."""
    url = re.escape(FIGMA_BASE + uuid)
    pattern = re.compile(
        r'<img\b(?:(?!>).|\n)*?\bsrc="' + url + r'"(?:(?!>).|\n)*?>',
        re.IGNORECASE,
    )
    return pattern.sub(lambda _m: replacement, html)


def replace_img_src_only(html: str, uuid: str, new_src: str) -> str:
    """Keep <img> attributes (e.g. class=\"photo\"); only swap src URL."""
    url = re.escape(FIGMA_BASE + uuid)
    pattern = re.compile(
        r'(<img\b(?:(?!>).|\n)*?\bsrc=")' + url + r'("(?:(?!>).|\n)*?>)',
        re.IGNORECASE,
    )
    return pattern.sub(r"\1" + new_src + r"\2", html)


def cart_btn_svg(w: int) -> str:
    return (
        f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<use href="#icon-cart-white" width="24" height="24" /></svg>'
    )


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")

    if 'id="icon-cb-solid-on"' not in html:
        html = html.replace("<body>", "<body>\n" + SPRITE, 1)

    html = html.replace('fill="#1C1C25" "=""></path>', 'fill="#1C1C25"></path>')

    html = re.sub(
        r'<div class="checkout-amount-line">\s*<span class="checkout-amount-line__label checkout-amount-line__label--info">\s*平台費\s*</span>\s*</span>',
        '<div class="checkout-amount-line">\n                  <span class="checkout-amount-line__label checkout-amount-line__label--info">平台費</span>',
        html,
        count=1,
    )

    html = html.replace(
        """              <img
                class="chev"
                src="https://www.figma.com/api/mcp/asset/06af69a2-603f-404e-acdc-00fc8e403523"
                alt=""
                id="toggle-hktvmall"
              />""",
        '<svg class="chev" id="toggle-hktvmall" viewBox="0 0 12 8" width="11" height="6" aria-hidden="true" focusable="false">'
        '<use href="#icon-chev-down-white" width="12" height="8" /></svg>',
        1,
    )
    html = html.replace(
        '<img class="chev merchant-chev" src="https://www.figma.com/api/mcp/asset/06af69a2-603f-404e-acdc-00fc8e403523" alt="" id="toggle-merchant-chev" />',
        '<svg class="chev merchant-chev" id="toggle-merchant-chev" viewBox="0 0 12 8" width="11" height="6" aria-hidden="true" focusable="false">'
        '<use href="#icon-chev-down-white" width="12" height="8" /></svg>',
        1,
    )

    by_uuid = {
        "1292f4a8-2202-4ba0-947b-871e9744759d": '<svg width="19" height="12" viewBox="0 0 19 12" aria-hidden="true"><path fill="#000" d="M1 10V8h2v2H1zm4 0V5h2v5H5zm4 0V2h2v8H9zm4 0V6h2v4h-2zm4 0V4h2v6h-2z"/></svg>',
        "25b7c8aa-ec9e-404c-bcf0-9a8eb288dd28": '<svg width="17" height="12" viewBox="0 0 17 12" aria-hidden="true"><path fill="#000" d="M8.5 3c2.2 2.4 4 4.8 4 6.5a4 4 0 11-8 0c0-1.7 1.8-4.1 4-6.5zm0 2.2a2.3 2.3 0 100 4.6 2.3 2.3 0 000-4.6z"/></svg>',
        "d98bc7fb-be70-4cbe-bb7c-2b63aded3261": '<svg width="27" height="13" viewBox="0 0 27 13" aria-hidden="true"><rect x="1" y="2" width="22" height="9" rx="2" fill="none" stroke="#000" stroke-width="1.2"/><rect x="24" y="5" width="2" height="3" rx="0.5" fill="#000"/><rect x="3" y="4" width="16" height="5" rx="1" fill="#000"/></svg>',
        "fff61bf6-fd28-4eee-b59d-6652d6838905": "",
        "5d8b5b28-ba44-41c8-9964-6d5d2bcaf3ba": "",
        "88274e6e-4039-46bc-91b8-ee240bbf501e": "",
        "dcb92bd8-317e-485c-b0eb-e9e972f692b2": '<svg class="cb-checked-art" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-cb-solid-on" width="24" height="24" /></svg>',
        "6efa2acb-5b2f-4966-8028-f724e1930066": "",
        "a64714aa-7447-4d2e-80dd-2e38ad16f43e": '<svg class="cb-checked-art cb-checked-art--header" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-cb-header-on" width="24" height="24" /></svg>',
        "2371ee45-a8bd-4b8f-a7cc-f00b4aa32f30": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-store" width="24" height="24" /></svg>',
        "ed3205a8-dce6-4673-9295-6e0ed69e72cd": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-truck" width="24" height="24" /></svg>',
        "14171d16-8be4-4bf2-805f-c8cc3ef90fc9": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-info" width="24" height="24" /></svg>',
        "315c3f54-112c-415a-9f97-c30dd21ef212": '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><use href="#icon-chev-small" width="16" height="16" /></svg>',
        "47c8317a-d346-4042-a751-0256aa41fdf6": '<svg class="cb-checked-art" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-cb-solid-on" width="24" height="24" /></svg>',
        "b2b638f7-41b0-4891-9dea-6ba85354ebc9": "",
        "ed602c61-f464-40e5-9c71-3f76bcccf1d0": '<svg class="merchant-threshold__ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-alert" width="24" height="24" /></svg>',
        "027f5248-15e2-4229-b63f-d868ec5f3869": '<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-chev-right" width="24" height="24" /></svg>',
        "88ec4636-f9b5-4dc2-9231-febb11d18152": '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-heart" width="24" height="24" /></svg>',
        "2690a13b-1911-428a-a6b1-4c1fb28ac803": '<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-trash" width="24" height="24" /></svg>',
        "52776fe8-4b85-4111-91b4-1fa87bc2e592": '<svg class="np-promo-decor" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-promo-tag" width="24" height="24" /></svg>',
        "2432f67a-431d-4dc9-91de-d38620c6bb98": '<svg class="inspire-promo-corner" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"><use href="#icon-promo-corner" width="24" height="24" /></svg>',
        "4acc4842-798e-4600-a002-72bf00b60767": cart_btn_svg(20),
        "eeb7f1b5-509a-4d80-83b8-7d1319fb4266": cart_btn_svg(20),
        "c8482275-00ed-412f-bbce-54bcfad53d2e": '<svg class="total__chev" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-chev-up" width="24" height="24" /></svg>',
        "ea46c064-dfa6-4374-bb47-c54de3cbe975": '<svg class="checkout-confirm-grabber" width="48" height="6" viewBox="0 0 48 6" aria-hidden="true" focusable="false"><use href="#icon-grabber" width="48" height="6" /></svg>',
        "e21a2740-5c53-4f48-ae0e-10a057318611": '<svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-close" width="24" height="24" /></svg>',
        "1769f912-2a41-4670-a87b-4cddea24c53e": '<svg class="checkout-confirm-chevron" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-chev-right" width="24" height="24" /></svg>',
    }

    photo_uuids = [
        "6ec7340d-3e93-407e-b117-89e9ea97e4c0",
        "ff5b7439-22f3-4d41-bb96-fe8c771eee3c",
        "f4e65fb8-e453-4b43-bab4-3bc32556f915",
        "4b3a634e-a4d2-4b8e-b035-d1316e34b225",
        "202d3315-01b6-44a8-bdcb-8065d11a691c",
        "a1b8eb76-6428-45b3-a065-2d1333b8e52c",
        "1bd0ddc3-e075-430c-9cd7-8fdbd3915624",
        "c27b5953-fa69-4062-b81f-28f2cd0704cc",
        "978ea72a-2abb-4716-9ed4-530e3d690836",
        "4ed9bd83-2aea-4385-8eda-fd5ebf3265a1",
        "61690ec0-ca52-48d2-8cad-0ebbfab679d7",
        "d42715fc-a0c1-4d21-a0ec-4156c46209db",
        "15b73d85-61d0-4e6f-bae7-c842f61467c6",
        "f1851296-dc0d-4e34-910a-6a8a1e3fd92d",
        "862248a7-324b-4fb1-be27-e6dbd1a73870",
        "1cfd5b37-e2b2-408e-9924-b30ddc54aeb6",
        "62cecc19-3bbf-4531-8785-e7b3cd41df3e",
        "61fde1a5-9946-425f-b58a-33afe1b4042a",
        "f536c3dd-2007-48bf-8937-ea1f60166f86",
        "07487bf4-ac70-49b5-8fd4-4df3187b3cbe",
        "d9dcbf59-795f-4dce-9409-7185864acb0e",
        "5c7578f2-afd4-4cc4-906e-89f2f5525342",
    ]
    # Cart / section product thumbnails — same order as HKTVmall Shopping Cart Figma (node 15619:11971)
    figma_cart_photos = [
        "https://www.figma.com/api/mcp/asset/3d80fc35-9fd2-4227-9376-1cca1da7225f",
        "https://www.figma.com/api/mcp/asset/67180cdf-f4c2-4664-847d-d4a34ab9d93e",
        "https://www.figma.com/api/mcp/asset/b64e4ffa-9914-4c16-9e1d-03e23685f3c6",
        "https://www.figma.com/api/mcp/asset/b5422bd0-c534-44fb-a162-cc3939334981",
        "https://www.figma.com/api/mcp/asset/2bdb7ab1-b5ce-4dae-8f6f-496a2e9240a3",
        "https://www.figma.com/api/mcp/asset/b92ce507-3ad3-4ed1-ad03-c3a4220803c8",
        "https://www.figma.com/api/mcp/asset/c04bc774-d161-46b7-a7ed-e13ab6cc9560",
        "https://www.figma.com/api/mcp/asset/c8ff5440-6cdd-48d2-83d6-9b73f879f9c8",
        "https://www.figma.com/api/mcp/asset/1e33e776-d661-4c9c-bec6-2b56638a4db8",
        "https://www.figma.com/api/mcp/asset/90b5f6fc-0a21-4a12-9b1a-69b85803e8d3",
        "https://www.figma.com/api/mcp/asset/2ac32b91-7edf-4ef4-9e22-5abd48850eef",
        "https://www.figma.com/api/mcp/asset/f94e7c45-cf0c-47d0-928f-89a8045226a5",
        "https://www.figma.com/api/mcp/asset/4fa9fbbe-b35a-4549-99a8-a4ab3abc7bac",
        "https://www.figma.com/api/mcp/asset/51926867-2b2a-40eb-b21a-df2dd2079843",
        "https://www.figma.com/api/mcp/asset/7922fd58-0d6a-4f67-853b-0901993b2ccd",
        "https://www.figma.com/api/mcp/asset/379d3162-f7c0-4bc5-a6aa-35136a3521f0",
        "https://www.figma.com/api/mcp/asset/47916c17-d6cf-494f-8e9b-22f63ea83549",
        "https://www.figma.com/api/mcp/asset/fe7ca429-de74-404c-bcfe-4224be6bc08a",
        "https://www.figma.com/api/mcp/asset/35015847-4084-4768-8f77-bacb244830de",
        "https://www.figma.com/api/mcp/asset/9fdc90e0-9e29-41c5-9808-ae9f5c454348",
        "https://www.figma.com/api/mcp/asset/bfba6cbd-f418-4b5a-883b-c403f0172f3c",
        "https://www.figma.com/api/mcp/asset/a95e345c-2c39-4883-8421-1bca313cf8e5",
    ]
    for i, u in enumerate(photo_uuids):
        html = replace_img_src_only(html, u, figma_cart_photos[i])

    for uuid, rep in by_uuid.items():
        html = replace_all_img(html, uuid, rep)

    # Same Figma UUID as HKTVmall threshold .ico; merchant row needs .merchant-threshold__ico sizing.
    html = html.replace(
        '<div class="merchant-threshold__row merchant-threshold__row--delivery">\n                    <svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-info"',
        '<div class="merchant-threshold__row merchant-threshold__row--delivery">\n                    <svg class="merchant-threshold__ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#icon-info"',
        1,
    )

    # Icons are inlined above; product photos intentionally use Figma MCP asset URLs (refresh from design if expired).

    INDEX.write_text(html, encoding="utf-8")
    print("OK", INDEX)


if __name__ == "__main__":
    main()
