#!/usr/bin/env python3

import pytest

import pathlib
import json

TESTVECTORS_PATH = pathlib.Path(__file__).parent.joinpath("testvectors.json")

# from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple, TypeVar, Union
from typing import List, Tuple

from bip39 import (
    encode_bytes,
    decode_phrase,
    phrase_to_seed,
    EncodingError,
    DecodingError,
)

########################################################################################################################
### Testcases encoding and decoding of BIP39 mnemonic phrases ##########################################################
########################################################################################################################


def load_test_vectors() -> List[Tuple[bytes, str, str]]:
    """Load the BIP39 test vectors from local storage.
    Original source for test vectors: https://github.com/trezor/python-mnemonic/blob/master/vectors.json
    """
    with open(TESTVECTORS_PATH) as f:
        vectors = json.load(f)
    return [(bytes.fromhex(entropy), phrase, seed) for entropy, phrase, seed, _ in vectors["english"]]


TEST_VECTORS = load_test_vectors()


@pytest.mark.parametrize("entropy, phrase, seed", TEST_VECTORS)
def test_encode_bytes__official_vectors(entropy: bytes, phrase: str, seed: str):
    assert encode_bytes(entropy) == phrase


@pytest.mark.parametrize("entropy, phrase, seed", TEST_VECTORS)
def test_decode_phrase__official_vectors(entropy: bytes, phrase: str, seed: str):
    assert decode_phrase(phrase) == entropy


@pytest.mark.parametrize("entropy, phrase, seed", TEST_VECTORS)
def test_seed_phrase__official_vectors(entropy: bytes, phrase: str, seed: str):
    assert phrase_to_seed(phrase, passphrase="TREZOR").hex() == seed


### Additional tests ###

PHRASES = [
    "any pitch edit post web arm gun cradle goose card aim absorb",
    "key water you run rent pen hub key learn tank sunset air echo letter adapt",
    "pupil year card short mean weird inch shy fun bid joy slot only use cry gap fox aisle",
    "jar kite sand indoor crowd spot label aim clay mix job gas kite can bomb wink ten emerge fly car also",
    "eight era guard oak fox rent day fee pool kid noble one pact bag slab april ugly job law razor blur try dose quiz",
]

PHRASES_INVALID_LENGTH = [" ".join(["any"] * i) for i in range(1, 65) if i not in {12, 15, 18, 21, 24}]

PHRASES_INVALID_CHECKSUM = [
    "any pitch edit post web arm gun cradle goose card aim abuse",
    "key water you run rent pen hub key learn tank sunset air echo letter add",
    "pupil year card short mean weird inch shy fun bid joy slot only use cry gap fox alarm",
    "jar kite sand indoor crowd spot label aim clay mix job gas kite can bomb wink ten emerge fly car alter",
    "eight era guard oak fox rent day fee pool kid noble one pact bag slab april ugly job law razor blur try dose quit",
]

PHRASES_INVALID_LENGTH_VALID_CHECKSUM = [
    "",
    "easy swamp table",
    "master auction transfer old lesson chief",
    "fuel absurd regular mandate kingdom valley miss start away",
    "achieve potato wine chase erupt machine quality ozone brick state attract equal "
    "canvas city weather infant acid stable grocery interest cruel diagram bid guide "
    "nut minimum broccoli",
    "truth rely once wild toast oxygen birth ugly spawn journey finger steak "
    "liberty tank fashion garbage swift bike safe rate since always attract chef "
    "final film clutch talk isolate tide",
    "chef recall shield table almost athlete barely absorb control oval vehicle proud "
    "debate rally vapor barely pioneer lion state chest fine volume comic romance "
    "cigar answer thing struggle mad abandon prefer bronze minor",
    "tail obey flash palace furnace blast faculty narrow number imitate slab state "
    "copper sister media ski dose achieve glad dirt want nasty giggle arrive "
    "grit fame parent oil mix mean repeat wealth summer daughter strategy corn",
    "honey walk trouble embark curious nation twin make dress smoke novel tank "
    "manage improve math tone sea purpose ozone junk rate language play milk "
    "term tray breeze skate couple barrel find void retire rapid armor brisk "
    "guess pistol desk",
    "accident purpose arm private excuse mesh useless depth party check drill inhale "
    "pink caught clerk minor uphold crush snack glory enforce hedgehog jealous prevent "
    "object ethics stage faith wage require turtle truth picture stove disease struggle "
    "strike gadget stereo beauty bachelor promote",
    "wisdom multiply crazy embrace connect wave toast shallow marine exchange frequent grief "
    "mouse genius where play twin romance lecture lunch rather pattern deer dinner "
    "romance jealous mutual food faint bamboo dignity carpet rice wisdom minimum offer "
    "drastic ready arm estate bulk squirrel goose square creek",
    "walnut cattle virtual admit fiction kitchen alpha fiction pudding mirror egg target "
    "grace snake casino pigeon hazard afford bulk estate maze rival prosper vibrant "
    "wrong begin wheel wear accident anger hip length chimney royal primary library "
    "frequent member gym phone result noodle unique design slice already display match",
]

PHRASES_INVALID_WORDS = [
    "any pitch edit post web arm gun cradle goose card aim abrasivo",
    "key water you run rent pen hub key learn tank sunset air echo letter activo",
    "pupil year card short mean weird inch shy fun bid joy slot only use cry gap fox adopter",
    "jar kite sand indoor crowd spot label aim clay mix job gas kite can bomb wink ten emerge fly car allagato",
    "eight era guard oak fox rent day fee pool kid noble one pact bag slab april ugly job law razor blur try dose peón",
]


@pytest.mark.parametrize("phrase", PHRASES)
def test_encode_decode(phrase: str):
    entropy = decode_phrase(phrase)
    assert encode_bytes(entropy) == phrase


@pytest.mark.parametrize(
    "num_bytes, num_words",
    ((bits // 8, num_words) for bits, num_words in [(128, 12), (160, 15), (192, 18), (224, 21), (256, 24)]),
)
def test_encode_bytes__valid_length(num_bytes: int, num_words: int):
    phrase = encode_bytes(b"\x00" * num_bytes)
    assert len(phrase.split()) == num_words


@pytest.mark.parametrize(
    "num_bytes", (num_bytes for num_bytes in range(64) if num_bytes * 8 not in {128, 160, 192, 224, 256})
)
def test_encode_bytes__invalid_length(num_bytes: int):
    with pytest.raises(EncodingError):
        encode_bytes(b"\x00" * num_bytes)


@pytest.mark.parametrize("phrase", PHRASES_INVALID_LENGTH)
def test_decode_phrase__invalid_length(phrase: str):
    with pytest.raises(DecodingError):
        decode_phrase(phrase)


@pytest.mark.parametrize("phrase", PHRASES_INVALID_CHECKSUM)
def test_decode_phrase__invalid_checksum(phrase: str):
    with pytest.raises(DecodingError):
        decode_phrase(phrase)


@pytest.mark.parametrize("phrase", PHRASES_INVALID_WORDS)
def test_decode_phrase__invalid_words(phrase: str):
    with pytest.raises(DecodingError):
        decode_phrase(phrase)

