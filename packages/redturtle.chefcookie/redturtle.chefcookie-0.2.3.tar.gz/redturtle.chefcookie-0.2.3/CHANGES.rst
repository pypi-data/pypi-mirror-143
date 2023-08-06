Changelog
=========

0.2.3 (2022-03-24)
------------------

- add flag to control panel that allow to enable cookie banner
- add cookie prefix to control panel to control the js plugin option
- allow to select endpoint for consent registry
- add domain whitelist so in case you have site with multiple domain can show 
  the banner in selected domain
- add matomo
- some minor fix to prevent cases where site editor remove configuration lines 
  partially
- add log tracking to new introduced actions
- Fix problem loading twitter timeline in tile manager from
  redturtle.tiles.management
  [lucabel]
- Do not use $ but vanilla javascript for old Plone sites compatibility.
  [cekk]


0.2.2 (2022-01-27)
------------------

- Align text with label of buttons.
- Removed cookie_setting_open button when only_technical_cookies is checked.
  [eikichi18]


0.2.1 (2022-01-11)
------------------

- Fix layers in adapters.
  [cekk]

0.2.0 (2022-01-11)
------------------

- Add facebook script manually (copied from original chefcookie script).
  [cekk]
- Allow to handle social based on link/script like twitter timeline
  [lucabel]


0.1.3 (2022-01-10)
------------------

- Remove YouTube unused field.
  [cekk]


0.1.2 (2022-01-10)
------------------

- Fix accept_iframe loading.
  [cekk]

0.1.1 (2022-01-10)
------------------

- Fix domain names when saving cookie settings.
  [cekk]


0.1.0 (2022-01-10)
------------------

- Initial release.
  [cekk, lucabel]
