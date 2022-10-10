import pytest

from helpers import *


@pytest.mark.parametrize('pattern, text ,expected', [
    ('(^|\s)(пив(о|ас|чик|андрий)|виск(и|ар)|вод(к|очк|яночк)|ром(|а|у)$|конья(к|чо)|бухл(о|ишко)|текил|вин(о|ишко))',
     'пивасик', True),
    ('(^|\s)(пив(о|ас|чик|андрий)|виск(и|ар)|вод(к|очк|яночк)|ром(|а|у)$|конья(к|чо)|бухл(о|ишко)|текил|вин(о|ишко))',
     'hello', False),
])
def test_mach_intent(pattern, text, expected):
    result = match_intent(pattern, text)
    assert result == expected


if __name__ == '__main__':
    p = '(^|\s)(пив(о|ас|чик|андрий)|виск(и|ар)|вод(к|очк|яночк)|ром(|а|у)$|конья(к|чо)|бухл(о|ишко)|текил|вин(о|ишко))'
    test_mach_intent(pattern=p, text='пивасик', expected=True)
