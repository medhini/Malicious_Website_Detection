%This is an examplar file on how the MLKNN program could be used (The main function is "MLKNN_train.m" and "MLKNN_test.m")
%
%Type 'help MLKNN_train' and 'help MLKNN_test' under Matlab prompt for more detailed information


% Loading the file containing the necessary inputs for calling the MLKNN function
load('sample data.mat'); 

%Set parameters for the MLKNN algorithm
Num=10;
Smooth=1; % Set the number of nearest neighbors considered to 10 and the smoothing parameter to 1

% Calling the main functions
[Prior,PriorN,Cond,CondN]=MLKNN_train(train_data,train_target,Num,Smooth); % Invoking the training procedure

[HammingLoss,RankingLoss,OneError,Coverage,Average_Precision,Outputs,Pre_Labels]=MLKNN_test(train_data,train_target,test_data,test_target,Num,Prior,PriorN,Cond,CondN); % Performing the test procedure