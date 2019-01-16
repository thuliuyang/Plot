function createfigure
%CREATEFIGURE(ZDATA1, YDATA1, XDATA1, CDATA1)

MatTemp=xlsread('data.xlsx','比值','C2:K7');
name = 'meic_jjj';

XData1=zeros(9,1);
for i=1:9
    XData1(i,1)=i
end
YData1=zeros(6,1)
for j=1:6
    YData1(j,1)=j
end
 %CTemp=struct2cell(MatTemp)
 CData1=MatTemp
 ZData1 = zeros(1,1)
%----------------------

% Create figure

figure1 = figure('PaperType','A4',...
    'Color',[1 1 1]);

% Create axes
axes1 = axes('Parent',figure1 ,...
    'YTickLabel',{'电力','工业','民用','交通','农业','总计'},...
    'YTick',[0.5 1.5 2.5 3.5 4.5 5.5 ],...
    'YDir','reverse',...
    'XTickLabel',{'SO_2','NO_X','CO','VOC','NH_3','PM_{10}','PM_{2.5}','BC','OC'},...
    'XTick',[0.5 1.5 2.5 3.5 4.5 5.5 6.5 7.5 8.5],...
    'XAxisLocation','top',...
    'Position',[0.081865678438074 0.320445468509985 0.857153110047846 0.591298701298701],...
    'FontSize',14,...
    'FontName','LucidaSansRegular',...
    'DataAspectRatio',[3 8 1],...
    'AlimMode', 'manual', ...
    'Box', 'on', ...
    'Layer', 'bottom', ...
    'PlotBoxAspectRatioMode','auto',...
    'CLim',[0 10]);
% Uncomment the following line to preserve the X-limits of the axes
 xlim(axes1,[0 9]);
% Uncomment the following line to preserve the Y-limits of the axes
 ylim(axes1,[0 6]);
box(axes1,'on');
hold(axes1,'all');

%----------------------
nanclr = [0.5 0.5 0.5];
 CData1(CData1 <0 ) = nan;
 amin=min(min(CData1));
 amax=max(max(CData1));

 cm = xlsread('data.xlsx','RGB','A4:C49');
 cm =flipud(cm);
 him = imagesc(CData1);
 set(him, 'XData', [0.5;8.5])
 set(him, 'YData', [0.5;5.5])
 
 n = size(cm,1);
 dmap=(amax-amin)/n;
 colormap([nanclr;cm]);
 caxis([amin-dmap, amax]);
 
h = colorbar;

caxis([0.4,1.5]);
h.Ticks = [0.5:0.25:1.5];

set(h,'location','eastoutside')


 if nargout >0
     h=him;
 end

for l = 0:9
    XL = [l,l]
    YL = [0,6]
    plot(XL,YL,'-k','LineWidth',0.1 )
end
for col = 0:6
    XL = [0,9]
    YL = [col,col]
    plot(XL,YL,'-k','LineWidth',0.1)
end

saveas(gcf ,['test.jpg'])



