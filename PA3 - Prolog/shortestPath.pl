%       8
%   m----->p
%   ^     ^
%  5 \    | 13
%     \   |
%       q
%       ^
%       | 3
%       |
%       k
%  ascii version

% Example Graph #1
arc(m,p,8).
arc(q,p,13).
arc(q,m,6).
arc(k,q,3).
% graph 2
arc(x,y,1000).
arc(x,z,2).
arc(x,w,2).
arc(w,y,1).
arc(z,y,2).
% there is a connnection between X and Y if there is a weighted edge between the two
connection(X,Y,W,[X,Y], _) :- arc(X,Y,W).
% member(term, list) -- succeeds if the term unifies with a member in the list
%  "\+" -- true if the goal cannot be proven
% member true if X exists in the list V
connection(X,Y,W,[X|P], V) :- \+ member(X,V),
  arc(X,Z,W1),
  connection(Z,Y,W2, P, [X|V]),
  W is W1 + W2.
% path(A,B,P) :- connection(A,B,_,P,[]).
% Get the Minimum of a list
% minl(List, Minimum).
minValue([SingleValueList], SingleValueList).
minValue([Start|End], Minimum) :-
  minValue(End, EndMinimum),
  Minimum is min(Start, EndMinimum).
% get the shortest path out of
% the possible path list
shortestPathValue(A,B,Path,Weight) :-
  %  list of all instances saitisyfin the goal for the template
  setof([P,L],pathShortest(A,B,P,L),List),
  List = [_|_],
  smallestWeight(List,[Path,Weight]).
% finding the minimum from set
% given path and Weight
smallestWeight([Left|Right],Min) :- minimum(Right,Left,Min).
% minimal path
% if there is only one value, it is the minimum
minimum([],EqualValue,EqualValue).
minimum([[Path,PossibleMin]|NextValue],[_,Min],Minimum) :-
  % if the value is lower than the current minimum
  PossibleMin < Min,
  % check the remaining values to see if there
  % lower than the current minimum
  currentMin(NextValue,[Path,PossibleMin],Minimum).
  % EndMinimum is min(Minimum, Minimum).
% min is "current minimum" Minimum is returned minimum
minimum([_|NextValue],Min,Minimum) :-
    minimum(NextValue,Min,Minimum).
% current min recursively runs the minimum to check
% all possible outcomes
currentMin(V1,[P,V2],M) :- minimum(V1,[P,V2],M).
% predicate to connect smallest weight to connection
pathShortest(A,B,P,L) :- connection(A,B,L,P,[]).
% connection(k,p,Weight,Path, []).
% path(k,p,Path, []).
path(A,B,P) :- shortestPathValue(A,B,P,_).
