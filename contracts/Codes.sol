// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract Codes is ERC721URIStorage {
  using Counters for Counters.Counter;
  Counters.Counter public _tokenIds;
  address public owner;

  mapping(uint256 => Code) private idToCode;

  struct Code {
    uint256 tokenId;
    address createdBy;
    address payable owner;
    bool isPrivate;
  }

  constructor() ERC721("Code", "CD") {
    owner = payable(msg.sender);
  }

  function createCode(string memory codeURI, bool isPrivate)
    public
    payable
    returns (uint256)
  {
    _tokenIds.increment();
    uint256 newTokenId = _tokenIds.current();

    _mint(msg.sender, newTokenId);
    _setTokenURI(newTokenId, codeURI);

    idToCode[newTokenId] = Code(newTokenId, msg.sender, payable(msg.sender), isPrivate);

    return newTokenId;
  }

  function transferCode(
    uint256 tokenId,
    address to
  ) public payable {
    require(msg.sender == idToCode[tokenId].owner, "Only owner can transfer code");
    require(msg.sender != to, "You can't transfer code to yourself");
    idToCode[tokenId].owner = payable(to);
    _transfer(msg.sender, to, tokenId);
//    emit Transfer(msg.sender, to, tokenId);
  }

  function fetchCodes() public view returns (Code[] memory) {
    uint itemCount = _tokenIds.current();

    Code[] memory codes = new Code[](itemCount);
    for (uint i = 0; i < itemCount; i++) {
      uint currentId = i + 1;
      Code storage currentCode = idToCode[currentId];
      if (currentCode.isPrivate == false || (currentCode.isPrivate == true && currentCode.owner == msg.sender)) {
        codes[i] = currentCode;
      }
    }
    return codes;
  }

  function fetchUserOwnerCodes(address user) public view returns (Code[] memory) {
    uint itemCount = _tokenIds.current();

    Code[] memory codes = new Code[](itemCount);
    for (uint i = 0; i < itemCount; i++) {
      uint currentId = i + 1;
      Code storage currentCode = idToCode[currentId];
      if (currentCode.owner == user) {
        if (currentCode.isPrivate == false || (currentCode.isPrivate == true && currentCode.owner == msg.sender)) {
          codes[i] = currentCode;
        }
      }
    }
    return codes;
  }

  function fetchCodesCreatedByUser(address user) public view returns (Code[] memory) {
    uint itemCount = _tokenIds.current();

    Code[] memory codes = new Code[](itemCount);
    for (uint i = 0; i < itemCount; i++) {
      uint currentId = i + 1;
      Code storage currentCode = idToCode[currentId];
      if (currentCode.createdBy == user) {
        if (currentCode.isPrivate == false || (currentCode.isPrivate == true && currentCode.owner == msg.sender)) {
          codes[i] = currentCode;
        }
      }
    }
    return codes;
  }

  function fetchCodesByToken(uint256[] calldata tokenIds) public view returns (Code[] memory) {
    uint itemCount = _tokenIds.current();

    Code[] memory codes = new Code[](itemCount);
    for (uint i = 0; i < itemCount; i++) {
      uint currentId = i + 1;
      Code storage currentCode = idToCode[currentId];
      for (uint j = 0; j < tokenIds.length; j++) {
        if (currentCode.tokenId == tokenIds[j]) {
          if (currentCode.isPrivate == false || (currentCode.isPrivate == true && currentCode.owner == msg.sender)) {
            codes[i] = currentCode;
          }
        }
      }
    }
    return codes;
  }

  function fetchCode(uint256 tokenId) public view returns (Code memory) {
    Code memory code = idToCode[tokenId];
    if (code.isPrivate == false || (code.isPrivate == true && code.owner == msg.sender)) {
      return code;
    } else {
      revert("Not found or private");
    }
  }
}
