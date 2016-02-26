<div class="header">
            
    <h1 class="page-title"><?php echo $this->lang->line('_MySQL All Running Indexes'); ?> <?php echo $this->lang->line('chart'); ?></h1>
</div>
        
<ul class="breadcrumb">
            <li><a href=""><?php echo $this->lang->line('home'); ?></a> <span class="divider">/</span></li>
            <li class="active"><?php echo $this->lang->line('_MySQL Monitor'); ?></li><span class="divider">/</span></li>
            <li class="active"><?php echo $this->lang->line('_MySQL All Running Indexes'); ?></li>
</ul>

<div class="container-fluid">
<div class="row-fluid">



<div class="ui-state-default ui-corner-all" style="height: 45px;" >
<p><span class="ui-icon ui-icon-search" style="float: left; margin-right: .3em;"></span>

<form name="form" class="form-inline" method="get" action="<?php site_url('lp_mysql/all_running_indexes') ?>" >
  <input type="hidden" name="search" value="submit" />

  <select name="server_id" class="input-small" style="width: 200px;">
  <option value="-1" ><?php echo $this->lang->line('host'); ?></option>
  <?php foreach ($dbserver as $k =>$v):?>
        <?php if( is_array( $v ) ):?>
        <?php foreach($v as $w=>$x):?>
                <option value=<?php echo $x["id"];?> <?php if($server_id==$x["id"]) echo "selected";?>> <?php echo $x["tags"] ?></option>;
  	<?php endforeach?>
        <?php endif?>
  <?php endforeach?>
  </select>
  
  
  <select name="index" class="input-small" style="width: 250px;">
  <option value="id" ><?php echo $this->lang->line('index'); ?></option>
  <?php foreach ($indexes as $k =>$v):?>
        <?php if( is_array( $v ) ):?>
        <?php foreach($v as $w=>$x):?>
                <option value=<?php echo $x["column_name"];?> <?php if($index==$x["column_name"]) echo "selected";?>> <?php echo $x["column_name"] ?></option>;
        <?php endforeach?>
        <?php endif?>
  <?php endforeach?>
  </select>

  <select name="time" class="input-small" style="width: 110px;">
  <option value="0" ><?php echo $this->lang->line('time'); ?></option>
  <option value=60 <?php if($time==60) echo "selected"; ?> >1 <?php echo $this->lang->line('date_hours'); ?></option>
  <option value=360 <?php if($time==360) echo "selected"; ?> >6 <?php echo $this->lang->line('date_hours'); ?></option>
  <option value=720 <?php if($time==720) echo "selected"; ?> >12 <?php echo $this->lang->line('date_hours'); ?></option>
  <option value=1440 <?php if($time==1440) echo "selected"; ?> >1 <?php echo $this->lang->line('date_days'); ?></option>
  <option value=4320 <?php if($time==4320) echo "selected"; ?> >3 <?php echo $this->lang->line('date_days'); ?></option>
  <option value=10080 <?php if($time==10080) echo "selected"; ?> >1 <?php echo $this->lang->line('date_weeks'); ?></option>
  </select>

  <button type="submit" class="btn btn-success"><i class="icon-search"></i> <?php echo $this->lang->line('search'); ?></button>

</form>
</div>

</div> <!-- /toolbar -->              
<hr/>

<div id="all_running_indexes" style="margin-top:5px; margin-left:0px; width:1500px; height:380px;"></div>

<script type="text/javascript" src="./lib/jqplot/jquery.jqplot.min.js"></script>
<script type="text/javascript" src="./lib/jqplot/plugins/jqplot.canvasTextRenderer.min.js"></script>
<script type="text/javascript" src="./lib/jqplot/plugins/jqplot.canvasAxisLabelRenderer.min.js"></script>
<script type="text/javascript" src="./lib/jqplot/plugins/jqplot.dateAxisRenderer.min.js"></script>
<script type="text/javascript" src="./lib/jqplot/plugins/jqplot.highlighter.min.js"></script>
<script type="text/javascript" src="./lib/jqplot/plugins/jqplot.cursor.min.js"></script>
<link href="./lib/jqplot/jquery.jqplot.min.css"  rel="stylesheet">

<script>

$(document).ready(function(){
  var data1=[
    <?php if(!empty($chart_reslut)) { foreach($chart_reslut as $item){ ?>
    ["<?php echo $item['time']?>", <?php echo $item['index']?> ],
    <?php }}else{ ?>
    []    
    <?php } ?>
  ];
  var plot1 = $.jqplot('all_running_indexes', [data1], {
    seriesDefaults: {
          rendererOptions: {
              smooth: true
          }
    },
    title:{
         text:"<?php echo $cur_server; ?> <?php echo $index; ?> <?php echo $this->lang->line('chart'); ?>",
         show:true,
         fontSize:'13px',
         textColor:'#666',
    },
    axes:{
        xaxis:{
            renderer:$.jqplot.DateAxisRenderer,
            tickOptions:{formatString:"<?php echo $chart_option['formatString']; ?>"},
            tickInterval:"",
            label: "",
        },
        yaxis: {  
                renderer: $.jqplot.LogAxisRenderer,
                tickOptions:{ suffix: '' } 
        } 
    },
    highlighter: {
            show: true, 
            showLabel: true, 
            tooltipAxes: '',
            sizeAdjust: 7.5 , tooltipLocation : 'ne'
    },
    cursor:{
            show: true, 
            zoom: true
    },
    series:[{showMarker:false, lineWidth:2, markerOptions:{style:'filledCircle'}}]
  });
//	console.log(data1.toString());
});

</script>


