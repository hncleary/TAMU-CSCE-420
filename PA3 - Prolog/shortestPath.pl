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
arc(q,m,5).
arc(k,q,3).




% there is a connnection between X and Y if there is a weighted edge between the two
connection(X,Y,W,[X,Y], _) :- arc(X,Y,W).
% member(term, list) -- succeeds if the term unifies with a member in the list
%  "\+" -- true if the goal cannot be proven
connection(X,Y,W,[X|P], V) :- \+ member(X,V),
  arc(X,Z,W1),
  connection(Z,Y,W2, P, [X|V]),
  W is W1 + W2.

% path(A,B,[A,B], _) :- arc(A,B,W).
% path(A,B,[X|P], V) :- \+ member(X,V),
%   arc(A,C,W1),
%   path(C,B,W2, P, [X|V]),
%   W is W1 + W2.

path(A,B,P) :- connection(A,B,W,P,[]).
minPathWeight(A,B,P,W) :- connection(A,B,W,P,[]).

% connection(k,p,Weight,Path, []).
% path(k,p,Path, []).
