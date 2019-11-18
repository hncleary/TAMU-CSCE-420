%my_agent.pl

%   this procedure requires the external definition of two procedures:
%
%     init_agent: called after new world is initialized.  should perform
%                 any needed agent initialization.
%
%     run_agent(percept,action): given the current percept, this procedure
%                 should return an appropriate action, which is then
%                 executed.
%
% This is what should be fleshed out

init_agent:-
  format('\n=====================================================\n'),
  format('This is init_agent:\n\tIt gets called once, use it for your initialization\n\n'),
  format('=====================================================\n\n'),
  %assert all of the starting conditions for agent at initial point 1,1
  assert(agentPosition(1,1)),
  assert(agentDirection(1)),
  %assert(world_size(4)),
  assert(visited(yes,1,1)),
  assert(parent([1,1],[1,1])),
  assert(numberOfMoves(0)),
  assert(isWumpus(no)),
  assert(isHole(no,1,1)),
  assert(isGold(no)),
  assert(wumpusAlive(yes)),
  assert(secondPass(yes)),
  assert(secondPass(no)).

%run_agent(Percept,Action):-
run_agent(_, goforward ):-
  format('\n=====================================================\n'),
  format('This is run_agent(.,.):\n\t It gets called each time step.\n\tThis default one simply moves forward\n'),
  format('You might find "display_world" useful, for your debugging.\n'),
  display_world,
  format('=====================================================\n\n').



% a procedure is either static or dynamic
% :- dynamic likes/2. => declares likes with an arity of 2
% artiy is the number of arguments taken for a procedure
:- dynamic
agentPosition/2,
isHole/3,
isWumpus/3,
visited/3,
parent/2,
numberOfMoves/1,
isGold/1,
wumpusAlive/1,
wumpusFound/2.

:- dynamic
agentDirection/1,
nextMove/1,
secondPass/1.

%   Action is one of:
%     goforward: move one square along current orientation if possible
%     turnleft:  turn left 90 degrees
%     turnright: turn right 90 degrees
%     grab:      pickup gold if in square
%     shoot:     shoot an arrow along orientation, killing wumpus if
%                in that direction
%     climb:     if in square 1,1, leaves the cave and adds 1000 points
%                for each piece of gold
%
%   Percept = [Stench,Breeze,Glitter,Bump,Scream]
%             The five parameters are either 'yes' or 'no'.
