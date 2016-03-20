function [Prior,PriorN,Cond,CondN]=MLKNN_train(train_data,train_target,Num,Smooth)
%MLKNN_train trains a multi-label k-nearest neighbor classifier
%
%    Syntax
%
%       [Prior,PriorN,Cond,CondN]=MLKNN_train(train_data,train_target,num_neighbor)
%
%    Description
%
%       KNNML_train takes,
%           train_data   - An MxN array, the ith instance of training instance is stored in train_data(i,:)
%           train_target - A QxM array, if the ith training instance belongs to the jth class, then train_target(j,i) equals +1, otherwise train_target(j,i) equals -1
%           Num          - Number of neighbors used in the k-nearest neighbor algorithm
%           Smooth       - Smoothing parameter
%      and returns,
%           Prior        - A Qx1 array, for the ith class Ci, the prior probability of P(Ci) is stored in Prior(i,1)
%           PriorN       - A Qx1 array, for the ith class Ci, the prior probability of P(~Ci) is stored in PriorN(i,1)
%           Cond         - A Qx(Num+1) array, for the ith class Ci, the probability of P(k|Ci) (0<=k<=Num) i.e. k nearest neighbors of an instance in Ci will belong to Ci , is stored in Cond(i,k+1)
%           CondN        - A Qx(Num+1) array, for the ith class Ci, the probability of P(k|~Ci) (0<=k<=Num) i.e. k nearest neighbors of an instance not in Ci will belong to Ci, is stored in CondN(i,k+1)

    [num_class,num_training]=size(train_target);

%Computing distance between training instances

    str=version('-release');
    ver_num=str2num(str(3:4));
    if(ver_num>=8)
        userview=memory;
        max_mat_elements=(userview.MaxPossibleArrayBytes)/8;
        max_mat_elements=(max_mat_elements*0.2)/2;
    else
        max_mat_elements=5000*5000;
    end
    
    if(num_training*num_training<max_mat_elements)
        mat1=concur(sum(train_data.^2,2),num_training);
        mat2=mat1';
        dist_matrix=mat1+mat2-2*train_data*train_data';
        dist_matrix=sqrt(dist_matrix);
        for i=1:num_training
            dist_matrix(i,i)=realmax;
        end

        %Computing Prior and PriorN
        for i=1:num_class
            temp_Ci=sum(train_target(i,:)==ones(1,num_training));
            Prior(i,1)=(Smooth+temp_Ci)/(Smooth*2+num_training);
            PriorN(i,1)=1-Prior(i,1);
        end

        %Computing Cond and CondN
        Neighbors=cell(num_training,1); %Neighbors{i,1} stores the Num neighbors of the ith training instance
        for i=1:num_training
            [temp,index]=sort(dist_matrix(i,:));
            Neighbors{i,1}=index(1:Num);
        end

        temp_Ci=zeros(num_class,Num+1); %The number of instances belong to the ith class which have k nearest neighbors in Ci is stored in temp_Ci(i,k+1)
        temp_NCi=zeros(num_class,Num+1); %The number of instances not belong to the ith class which have k nearest neighbors in Ci is stored in temp_NCi(i,k+1)
        for i=1:num_training
            temp=zeros(1,num_class); %The number of the Num nearest neighbors of the ith instance which belong to the jth instance is stored in temp(1,j)
            neighbor_labels=[];
            for j=1:Num
                neighbor_labels=[neighbor_labels,train_target(:,Neighbors{i,1}(j))];
            end
            for j=1:num_class
                temp(1,j)=sum(neighbor_labels(j,:)==ones(1,Num));
            end
            for j=1:num_class
                if(train_target(j,i)==1)
                    temp_Ci(j,temp(j)+1)=temp_Ci(j,temp(j)+1)+1;
                else
                    temp_NCi(j,temp(j)+1)=temp_NCi(j,temp(j)+1)+1;
                end
            end
        end
        for i=1:num_class
            temp1=sum(temp_Ci(i,:));
            temp2=sum(temp_NCi(i,:));
            for j=1:Num+1
                Cond(i,j)=(Smooth+temp_Ci(i,j))/(Smooth*(Num+1)+temp1);
                CondN(i,j)=(Smooth+temp_NCi(i,j))/(Smooth*(Num+1)+temp2);
            end
        end
        
    else
        
        block_size=floor(max_mat_elements/num_training);
        num_blocks=ceil(num_training/block_size);
        
        %Computing Prior and PriorN
        for i=1:num_class
            temp_Ci=sum(train_target(i,:)==ones(1,num_training));
            Prior(i,1)=(Smooth+temp_Ci)/(Smooth*2+num_training);
            PriorN(i,1)=1-Prior(i,1);
        end
        
        Neighbors=cell(num_training,1); %Neighbors{i,1} stores the Num neighbors of the ith training instance
        temp_Ci=zeros(num_class,Num+1); %The number of instances belong to the ith class which have k nearest neighbors in Ci is stored in temp_Ci(i,k+1)
        temp_NCi=zeros(num_class,Num+1); %The number of instances not belong to the ith class which have k nearest neighbors in Ci is stored in temp_NCi(i,k+1)
        
        for iter=1:num_blocks
            low=block_size*(iter-1)+1;
            if(iter==num_blocks)
                high=num_training;
            else
                high=block_size*iter;
            end
            
            tmp_data=train_data(low:high,:);
            tmp_size=size(tmp_data,1);
            mat1=concur(sum(train_data.^2,2),tmp_size);
            mat2=concur(sum(tmp_data.^2,2),num_training)';
            tmp_dist_matrix=mat1+mat2-2*train_data*tmp_data';
            tmp_dist_matrix=sqrt(tmp_dist_matrix);
            tmp_dist_matrix=tmp_dist_matrix';
            
            for i=low:high
                tmp_dist_matrix(i-low+1,i)=realmax;
            end
            
            %Computing Cond and CondN
            for i=low:high
                [temp,index]=sort(tmp_dist_matrix(i-low+1,:));
                Neighbors{i,1}=index(1:Num);
            end
            
            for i=low:high
                temp=zeros(1,num_class); %The number of the Num nearest neighbors of the ith instance which belong to the jth class is stored in temp(1,j)
                neighbor_labels=[];
                for j=1:Num
                    neighbor_labels=[neighbor_labels,train_target(:,Neighbors{i,1}(j))];
                end
                for j=1:num_class
                    temp(1,j)=sum(neighbor_labels(j,:)==ones(1,Num));
                end
                for j=1:num_class
                    if(train_target(j,i)==1)
                        temp_Ci(j,temp(j)+1)=temp_Ci(j,temp(j)+1)+1;
                    else
                        temp_NCi(j,temp(j)+1)=temp_NCi(j,temp(j)+1)+1;
                    end
                end
            end
        end
        
        for i=1:num_class
            temp1=sum(temp_Ci(i,:));
            temp2=sum(temp_NCi(i,:));
            for j=1:Num+1
                Cond(i,j)=(Smooth+temp_Ci(i,j))/(Smooth*(Num+1)+temp1);
                CondN(i,j)=(Smooth+temp_NCi(i,j))/(Smooth*(Num+1)+temp2);
            end
        end        
    end