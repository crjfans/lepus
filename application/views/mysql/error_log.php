<div class="header">
            
            <h1 class="page-title"><?php echo $this->lang->line('mysql'); ?>  <?php echo $this->lang->line('_InnoDB Monitor'); ?></h1>
</div>
        
<ul class="breadcrumb">
            <li><a href="<?php echo site_url(); ?>"><?php echo $this->lang->line('home'); ?></a> <span class="divider">/</span></li>
            <li class="active"><?php echo $this->lang->line('_MySQL Monitor'); ?></li><span class="divider">/</span></li>
            <li class="active"><?php echo $this->lang->line('_MySQL Error Log'); ?></li>
            <span class="right"><?php echo $this->lang->line('the_latest_acquisition_time'); ?>:<?php if(!empty($datalist)){ echo $datalist[0]['create_time'];} else {echo $this->lang->line('the_monitoring_process_is_not_started');} ?></span>
</ul>

<div class="container-fluid">
<div class="row-fluid">
 
<script src="lib/bootstrap/js/bootstrap-switch.js"></script>
<link href="lib/bootstrap/css/bootstrap-switch.css" rel="stylesheet"/>
                    
<div class="ui-state-default ui-corner-all" style="height: 45px;" >
<p><span style="float: left; margin-right: .3em;" class="ui-icon ui-icon-search"></span>                 
<form name="form" class="form-inline" method="get" action="" >
  <input type="hidden" name="search" value="submit" />
  
  <input type="text" id="host"  name="host" value="" placeholder="<?php echo $this->lang->line('please_input_host'); ?>" class="input-medium" >
  <input type="text" id="tags"  name="tags" value="" placeholder="<?php echo $this->lang->line('please_input_tags'); ?>" class="input-medium" >
  <select name="error_level" class="input-small" style="width: 100px;">
      <option value=""><?php echo 'Error Level'; ?></option>
      <option value="0" <?php if($setval['error_level']=='0') echo "selected"; ?> ><?php echo 'Notice'; ?></option>
      <option value="1" <?php if($setval['error_level']=='1') echo "selected"; ?> ><?php echo 'Warning'; ?></option>
      <option value="2" <?php if($setval['error_level']=='2') echo "selected"; ?> ><?php echo 'Error'; ?></option>
  </select>
  
  <button type="submit" class="btn btn-success"><i class="icon-search"></i> <?php echo $this->lang->line('search'); ?></button>
  <a href="<?php echo site_url('lp_mysql/mysql_error_log') ?>" class="btn btn-warning"><i class="icon-repeat"></i> <?php echo $this->lang->line('reset'); ?></a>
  <button id="refresh" class="btn btn-info"><i class="icon-refresh"></i> <?php echo $this->lang->line('refresh'); ?></button>
</form>                
</div>


<div class="">
    <table id="error_log_table" class="table table-hover table-condensed  table-bordered">
      <thead>
       <tr style="font-size: 12px;">
	<th colspan="2"></th>
	<th colspan="3"><center>MySQL_Error_Log</center></th>
        <th colspan="3"><center>Process</center></th>
      </tr>
        <tr style="font-size: 12px;" >
        <th><center><?php echo $this->lang->line('host'); ?></center></th>
        <th><center><?php echo $this->lang->line('tags'); ?></center></th> 
        <th><center>error_level</center></th> 
        <th><center>error_event</center></th> 
        <th><center>change_time</center></th> 
        <th><center>remarks(双击更改)</center></th> 
        <th><center>process_user</center></th> 
        <th></th>
	    </tr>
      </thead>
      <tbody>
 <?php if(!empty($datalist)) {?>
 <?php foreach ($datalist  as $item):?>
    <tr 
        style="font-size: 12px;
        <?php 
            if ($item['is_processed']==0){
                if ($item['error_level']==1) 
                    echo 'color:Coral';
                else if($item['error_level']==2) 
                    echo 'color:red';
                else
                    echo 'color:DarkGreen';
            }
            else
                echo 'color:black';
        ?>
    ">
        <td style="display:none"><?php echo $item['id']; ?></td>
        <td><?php echo $item['host'] ?>:<?php echo $item['port'] ?></font></td>
        <td><?php echo $item['tags']; ?></td>
        <td>
            <?php 
                if ($item['error_level']==0) 
                    echo "Notice";
                else if ($item['error_level']==1)
                    echo "Warning";
                else if ($item['error_level']==2)
                    echo "Error";
                else echo "Unknown";
            ?>
        </td>
        <td width="60%"><?php echo $item['error_event'] ?></td>
        <td><?php echo $item['create_time'] ?></td>
        <td><?php echo $item['remarks'] ?></td>
        <td><?php echo $item['process_user'] ?></td>
	<td>
        <a href="<?php echo site_url('lp_mysql/mysql_error_log_delete/'.$item['id']) ?>" class="confirm_delete" title="<?php echo $this->lang->line('add_trash'); ?>" ><i class="icon-trash"></i></a>
        </td>
 <?php endforeach;?>
   <tr>
	<td colspan="9">
	<font style="<?php if($count>0)echo 'color:red' ;?>"><?php echo $this->lang->line('total_no_process_record'); ?> <?php echo $count; ?></font>
	</td>
   </tr>
 <?php }else{  ?>
   <tr>
	<td colspan="9">
	<font color="red"><?php echo $this->lang->line('no_record'); ?></font>
	</td>
   </tr>
 <?php } ?>


      </tbody>
    </table>
</div>

 <script type="text/javascript">
    $('#refresh').click(function(){
        document.location.reload(); 
    })
 </script>
<script type="text/javascript">
        $(' .confirm_delete').click(function(){
                return confirm("<?php echo $this->lang->line('add_to_trash_confirm'); ?>");     
        });
</script>

<script type="text/javascript">
        $(' .confirm_save').click(function(){
                return confirm("<?php echo $this->lang->line('save_to_db_confirm'); ?>");     
        });
</script>

</script>

        <script type="text/javascript">  
        function Edit_remarks(){  
            var rows=document.getElementById("error_log_table").rows;  
            if(rows.length>0){  
                for(var i=1;i<rows.length;i++){  
                  (function(i){  
                    var obj=rows[i].cells[6];  
                    obj.ondblclick=function()
		    {
			$(obj).attr('contentEditable',true);
			$(obj).focus();
			var_remarks_old=obj.innerHTML;
	            };  
		    obj.onblur=function(){
                    	var_id=$(rows[i].cells[0]).text();  
		    	my_url= "<?php echo site_url('lp_mysql/mysql_error_log_edit/')."/".$this->session->userdata('username'); ?>" +"/"+ var_id;
			var_remarks_new=$(obj).text();
			$(obj).attr('contentEditable',false);
			if(var_remarks_old !== var_remarks_new){
				
				if(var_remarks_new.length <= 20){
		        		my_url= my_url + "/" +var_remarks_new;
					window.location.href=my_url; 
				}
				else 
					alert("you just can input 20 words!");
			}
		    };
                    })(i)  
                }  
            }  
        }  
        window.onload=function(){Edit_remarks();}  
</script> 
