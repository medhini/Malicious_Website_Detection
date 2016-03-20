function Average_Precision=Average_precision(Outputs,test_target)
%Computing the average precision
%Outputs: the predicted outputs of the classifier, the output of the ith instance for the jth class is stored in Outputs(j,i)
%test_target: the actual labels of the test instances, if the ith instance belong to the jth class, test_target(j,i)=1, otherwise test_target(j,i)=-1

    [num_class,num_instance]=size(Outputs);
    temp_Outputs=[];
    temp_test_target=[];
    for i=1:num_instance
        temp=test_target(:,i);
        if((sum(temp)~=num_class)&(sum(temp)~=-num_class))
            temp_Outputs=[temp_Outputs,Outputs(:,i)];
            temp_test_target=[temp_test_target,temp];
        end
    end
    Outputs=temp_Outputs;
    test_target=temp_test_target;     
    [num_class,num_instance]=size(Outputs);
    
    Label=cell(num_instance,1);
    not_Label=cell(num_instance,1);
    Label_size=zeros(1,num_instance);
    for i=1:num_instance
        temp=test_target(:,i);
        Label_size(1,i)=sum(temp==ones(num_class,1));
        for j=1:num_class
            if(temp(j)==1)
                Label{i,1}=[Label{i,1},j];
            else
                not_Label{i,1}=[not_Label{i,1},j];
            end
        end
    end
    
    aveprec=0;
    for i=1:num_instance
        temp=Outputs(:,i);
        [tempvalue,index]=sort(temp);
        indicator=zeros(1,num_class);
        for m=1:Label_size(i)
            [tempvalue,loc]=ismember(Label{i,1}(m),index);
            indicator(1,loc)=1;
        end
        summary=0;
        for m=1:Label_size(i)
            [tempvalue,loc]=ismember(Label{i,1}(m),index);
            summary=summary+sum(indicator(loc:num_class))/(num_class-loc+1);
        end
        ap_binary(i)=summary/Label_size(i);
        aveprec=aveprec+summary/Label_size(i);
    end
    Average_Precision=aveprec/num_instance;