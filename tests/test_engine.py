import pytest

from engine import match_intent


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
    pytest.main()
