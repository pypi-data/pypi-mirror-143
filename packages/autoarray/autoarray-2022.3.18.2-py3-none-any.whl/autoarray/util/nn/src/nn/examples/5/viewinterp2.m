function [h] = viewinterp2(fin, fout, verbose)

    if nargin == 2
        verbose = 1;
    end
  
    if verbose
        fprintf('plotting data from "%s" and "%s"\n', fin, fout);
        fprintf('  reading "%s"...', fin);
    end

    data = load(fin);
    xin = data(:, 1);
    yin = data(:, 2);
    zin = data(:, 3);
    zmin = min(zin);
    zmax = max(zin);
    nz = length(zin);

    if verbose
        fprintf('\n  reading "%s"...', fout);
    end
  
    data = load(fout);
    x = data(:, 1);
    y = data(:, 2);
    z = data(:, 3);
    clear data;
  
    if verbose
        fprintf('\n');
    end

    if verbose
        fprintf('  working out the grid dimensions...')
    end
    n = length(x);
    if x(2) - x(1) ~= 0 & y(2) - y(1) == 0
        xfirst = 1;
        xinc = x(2) > x(1);
        if xinc
            nx = min(find(diff(x) < 0));
        else
            nx = min(find(diff(x) > 0));
        end
        if mod(n, nx) ~= 0
            error(sprintf('\n  Error: could not work out the grid size, n = %d, nx = %d, n / nx = %f\n', n, nx, n / nx));
        end
        ny = n / nx;
        x = x(1 : nx);
        y = y(1 : nx : n);
        z = reshape(z, nx, ny)';
    elseif x(2) - x(1) == 0 & y(2) - y(1) ~= 0
        xfirst = 0;
        yinc = y(2) > y(1);
        if yinc
            ny = min(find(diff(y) < 0));
        else
            ny = min(find(diff(y) > 0));
        end
        if mod(n, ny) ~= 0
            error(sprintf('\n  Error: could not work out the grid size, n = %d, ny = %d, n / ny = %.3f\n', n, ny, n / ny));
        end
        nx = n / ny;
        y = y(1 : ny);
        x = x(1 : ny : n);
        z = reshape(z, ny, nx);
    else
        error('  Error: not a rectangular grid');
    end
    if verbose
        if xfirst
            fprintf('%d x %d, stored by rows\n', nx, ny);
        else
            fprintf('%d x %d, stored by columns\n', nx, ny);
        end
    end
  
    if verbose
        fprintf(sprintf('  plotting "%s"...', fin));
    end

    map = colormap;
    hold on;
    for i = 1 : nz
        plot(xin(i), yin(i), '.', 'color', zcolor(zin(i), zmin, zmax, map), 'markersize', 2);
    end
    axis equal;
    axis tight;
    set(gca, 'box', 'on');

    if verbose
        fprintf(sprintf('\n  plotting "%s"...', fout));
    end

    dv = floor((zmax - zmin) / 15);
    V = [floor(zmin) : dv : ceil(zmax)];
    contour(x, y, z, V, 'k');

    if verbose
        fprintf('\n');
    end

    return
  
function c = zcolor(z, zmin, zmax, map)

    ind = floor((z - zmin) / (zmax - zmin) * 64 + 1);
    ind = min(ind, 64);
    c = map(ind, :);

    return
