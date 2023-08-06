# BattleNet Clients
BattleNet Clients provide a uniform interface for Blizzard's Battle.net Developer Rest Application Programming
Interface (BNET Rest API)

## Installation

Windows, OS X & Linux:

    pip install battlenet_client

## Clone
Clone the latest version: https://gitlab.com/battlenet1/battlenet-client.git

## Usage Example
    > from battlenet_client.wow.game_data import achievement_category
    > achievement_category('us', category_id=81)
    # ('https://us.api.blizzard.com/data/wow/achievement-category/81', {'locale': None, 'namespace': 'static-us'})


For more information, please the [wiki][wiki]

Note: This package is a dependency of my other [Battle.net REST API packages](https://gitlab.com/battlenet1)

## Release History
Please change log for complete history

## Meta

David "Gahd" Couples – [@gahdania][twitter] [Twitch][twitch] – gahdania@gahd.io

Distributed under the GPL v3+ license. See ``LICENSE`` for more information.

[Battle.net Client on Gitlab][gitlab]

## Contributing

1. [Fork it][fork]
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[wiki]: https://gitlab.com/battlenet1/battlenet-client/-/wikis/home
[twitter]: https://twitter.com/gahdania
[twitch]: https://www.twitch.tv/gahd
[gitlab]: https://gitlab.com/battlenet1/battlenet-client
[fork]: https://gitlab.com/battlenet1/battlenet-client/-/forks/new
