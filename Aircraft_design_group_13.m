#Hi
%% Flight Mission Profile Generator in MATLAB
% Genererar en ren och skarp flygprofil i läroboksstil
% Innehåller: Take-off, Cruise (konstant höjd), Descent, Loiter, Land, Diversion och Reserve

clear; clc; close all;

%% 1. Skapa figur
fig = figure('Name', 'Flight Mission Profile', ...
             'Color', 'w', ...
             'Position', [100, 100, 950, 680]);
ax = axes('Parent', fig);
hold(ax, 'on');

%% 2. Geometriska gränser för diagrammet
x_min = 5;   x_max = 95;
y_min = 0;   y_max = 90;

% Rektangulär ytterram
plot([x_min, x_max, x_max, x_min, x_min], ...
     [y_min, y_min, y_max, y_max, y_min], ...
     'k-', 'LineWidth', 1.6);

%% 3. Horisontella referenslinjer för flygnivåer (Flight Levels)
y_FL0   = 6;
y_FL15  = 16;
y_FL100 = 42;

% FL0 (Marknivå)
plot([x_min, x_max], [y_FL0, y_FL0], 'k:', 'LineWidth', 1.1);
text(40, y_FL0 + 2.2, 'FL0', 'FontName', 'Times New Roman', ...
     'FontSize', 11, 'FontWeight', 'bold', 'FontAngle', 'italic', 'HorizontalAlignment', 'center');

% FL15
plot([x_min, x_max], [y_FL15, y_FL15], 'k:', 'LineWidth', 1.1);
text(40, y_FL15 + 2.2, 'FL15', 'FontName', 'Times New Roman', ...
     'FontSize', 11, 'FontWeight', 'bold', 'FontAngle', 'italic', 'HorizontalAlignment', 'center');

% FL100
plot([x_min, x_max], [y_FL100, y_FL100], 'k:', 'LineWidth', 1.1);
text(40, y_FL100 + 2.2, 'FL100', 'FontName', 'Times New Roman', ...
     'FontSize', 11, 'FontWeight', 'bold', 'FontAngle', 'italic', 'HorizontalAlignment', 'center');

%% 4. Vertikala fasgränser (streckade linjer)
x_to_cr  = 25;  % Take-off -> Cruise
x_cr_de  = 47;  % Cruise -> Descent
x_de_lo  = 57;  % Descent -> Loiter
x_lo_la  = 67;  % Loiter -> Land
x_la_di  = 76;  % Land -> Diversion

phase_divs = [x_to_cr, x_cr_de, x_de_lo, x_lo_la, x_la_di];
for x = phase_divs
    plot([x, x], [y_min, y_max], 'k--', 'LineWidth', 1.0);
end

%% 5. Fasetiketter i toppen (vertikal text, 90 graders rotation)
font_opts = {'FontName', 'Times New Roman', 'FontSize', 12, ...
             'Rotation', 90, 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'left'};

text(9,  y_max - 5, 'Take-off',   font_opts{:});
text(28, y_max - 5, 'Cruise',     font_opts{:});
text(49, y_max - 5, 'Descent',    font_opts{:});
text(59, y_max - 5, 'Loiter',     font_opts{:});
text(69, y_max - 5, 'Land',       font_opts{:});
text(79, y_max - 5, 'Diversion',  font_opts{:});

%% 6. Flygprofilens bana (höjdkurva med konstant marschhöjd)
y_cruise = 74.0; % Konstant marschhöjd (ingen step-climb)

x_profile = [
     5.0, ...  % Start på marken
     8.0, ...  % Start av rullning / take-off
    11.5, ...  % Stigning till FL15
    15.0, ...  % Planflykt vid FL15
    19.5, ...  % Genomstigning FL100
    25.0, ...  % Nå marschhöjd
    47.0, ...  % Slut på marschhöjd (rak linje genom hela Cruise)
    57.0, ...  % Nå loiter-höjd (FL100)
    65.0, ...  % Slut på loiter / holding
    72.0, ...  % Sättning vid landning (FL0)
    76.0, ...  % Omdirigering / avbruten landning på marken
    82.5, ...  % Stigning till alternativ marschhöjd
    88.5, ...  % Diversion marsch slut
    93.5, ...  % Slutlig landning vid alternativ flygplats
    95.0       % Parkering
];

y_profile = [
    y_FL0, ...
    y_FL0, ...
    y_FL15, ...
    y_FL15, ...
    y_FL100, ...
    y_cruise, ...
    y_cruise, ...
    y_FL100, ...
    y_FL100, ...
    y_FL0, ...
    y_FL0, ...
    53.0, ...
    53.0, ...
    y_FL0, ...
    y_FL0
];

% Rita flygbanan med en distinkt solid svart linje
plot(x_profile, y_profile, 'k-', 'LineWidth', 2.4);

%% 7. Topp-pilar och vikter (TOW, Landing weight, ZFW)
draw_down_arrow(ax, 8.0,  y_max + 7.5, y_max, 'TOW');
draw_down_arrow(ax, 72.0, y_max + 7.5, y_max, 'Landing weight');
draw_down_arrow(ax, 93.5, y_max + 7.5, y_max, 'ZFW');

%% 8. Botten-dimensioner och klamrar (Main mission, Reserve, Diversion)
% Vertikala referenslinjer nedåt från ramen
plot([x_min, x_min], [y_min, -26], 'k-',  'LineWidth', 0.8);
plot([8.0,   8.0],   [y_min, -18], 'k-',  'LineWidth', 0.8);
plot([57.0,  57.0],  [y_min, -18], 'k:',  'LineWidth', 0.8);
plot([72.0,  72.0],  [y_min, -18], 'k-',  'LineWidth', 0.8);
plot([76.0,  76.0],  [y_min, -10], 'k-',  'LineWidth', 0.8);
plot([93.5,  93.5],  [y_min, -26], 'k-',  'LineWidth', 0.8);

% 1. Main mission (Take-off till Land)
draw_dimension_bracket(ax, 8.0, 72.0, -7.0, 'Main mission', false);

% 2. Diversion (inom diversion-fasen)
draw_dimension_bracket(ax, 76.0, 93.5, -7.0, 'Diversion', false);

% 3. Reserve (omfattar Loiter och Diversion)
draw_dimension_bracket(ax, 57.0, 93.5, -15.5, 'Reserve', true);

% 4. Total mission span
draw_dimension_bracket(ax, x_min, 93.5, -23.5, 'Flight time and fuel', false);

%% 9. Axelinställningar
xlim([0, 100]);
ylim([-30, 105]);
axis(ax, 'off');

%% 10. Exportera bildfil (avkommentera vid behov)
% exportgraphics(fig, 'flight_profile_matlab.png', 'Resolution', 300);
% exportgraphics(fig, 'flight_profile_matlab.pdf', 'ContentType', 'vector');


%% === HJÄLPFUNKTIONER ===

function draw_down_arrow(~, x, y_start, y_end, label_text)
    plot([x, x], [y_start, y_end], 'k-', 'LineWidth', 1.3);
    arr_w = 0.9;
    arr_h = 2.0;
    fill([x - arr_w, x + arr_w, x], ...
         [y_end + arr_h, y_end + arr_h, y_end], ...
         'k', 'EdgeColor', 'none');
    text(x, y_start + 1.2, label_text, ...
         'FontName', 'Times New Roman', 'FontSize', 12, ...
         'FontWeight', 'bold', 'FontAngle', 'italic', ...
         'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom');
end

function draw_dimension_bracket(~, x1, x2, y, label_text, is_bold)
    plot([x1, x2], [y, y], 'k-', 'LineWidth', 1.2);
    arr_w = 1.6;
    arr_h = 1.0;
    fill([x1, x1 + arr_w, x1 + arr_w], [y, y + arr_h, y - arr_h], 'k', 'EdgeColor', 'none');
    fill([x2, x2 - arr_w, x2 - arr_w], [y, y + arr_h, y - arr_h], 'k', 'EdgeColor', 'none');
     
    weight = 'normal';
    if is_bold
        weight = 'bold';
    end
    text((x1 + x2)/2, y + 1.2, label_text, ...
         'FontName', 'Times New Roman', 'FontSize', 11, ...
         'FontWeight', weight, ...
         'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom');
end
