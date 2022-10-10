// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract DecentraPoll {
    uint public id;

    struct Poll {
        uint256 id;
        string description;
        uint256 date;
        uint256 voteA;
        uint256 voteB;
    }

    Poll[] public polls;

    function addPoll(string memory _description) public returns (string memory) {
        Poll memory new_poll = Poll(id, _description, block.timestamp, 0, 0);
        id++;
        polls.push(new_poll);
        return new_poll.description;
    }

    function addVoteA(uint _id) public returns(uint256) {
        polls[_id].voteA += 1;
        return polls[_id].voteA;
    }

}